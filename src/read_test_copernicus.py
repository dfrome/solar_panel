"""
Reads files that werer downloaded from Copernicus and compares some values.
Because the parameter used to call the api changed at some time and I need to know whether the values are consistant
I use :
conda activate powerbi_env
"""
import xarray as xr
import pandas as pd
import os

folder = r'F:\projPerso\home_power\data\copernicus\fromAPIcompare'
nc_files = [f for f in os.listdir(folder) if f.endswith('.nc')]
total_files = len(nc_files)

"""
#df_list = []
for file in nc_files:
    path = os.path.join(folder, file)
    try:
        ds = xr.open_dataset(path)
        df = ds.to_dataframe().reset_index()
        df['source_file'] = file
        df['total_number_of_files'] = total_files
        #df_list.append(df)
        print(f'Successfully processed {file}')
        print(df.head(30))
    except Exception as e:
        print(f'Erreur avec {file}: {e}')
#if df_list:
#    dataset = pd.concat(df_list, ignore_index=True)
"""

def load_df(file):
    path = os.path.join(folder, file)
    try:
        ds = xr.open_dataset(path)
        df = ds.to_dataframe().reset_index()
        df['source_file'] = file
        return df
    except Exception as e:
        print(f'Error with {file}: {e}')
        return None


filename="old.nc"
file = os.path.join(folder, filename)
df_old = load_df(filename)

filename="new.nc"
file = os.path.join(folder, filename)
df_new = load_df(filename)
print("Old data:")
print(df_old.head(30))
print("\n\n\nNew data:")
#print(df_new.head(30))
df_new_tours = df_new[(df_new['latitude'] == 47.25) & (df_new['longitude'] == 0.75)]
print(df_new_tours.head(30))



# Now compare some values
merged = pd.merge(df_old, df_new_tours, on=['time', 'latitude', 'longitude'], suffixes=('_old', '_new'))
merged['difference'] = merged['ssrd_old'] - merged['ssrd_new']
print("Differences between old and new data:")
print(merged[['time', 'latitude', 'longitude', 'ssrd_old', 'ssrd_new', 'difference']].head(30))
print(f"Total differences found: {merged['difference'].abs().sum()}")

"""
Great, the discrepancies are statistically unsignificant (in the order of 1e-10), so both datasets can be considered equivalent for practical purposes.
"""