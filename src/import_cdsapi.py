""" using :
conda activate powerbi_env
"""

import cdsapi
import zipfile
import os

target_folder = r'.\data\copernicus\fromAPI01'
os.makedirs(target_folder, exist_ok=True)

"""
 For info, see https://cds.climate.copernicus.eu/datasets/sis-energy-derived-reanalysis?tab=download
 and search for "solar" on Copernicus site.
 Worked for 07->12 2024 and 01 2025 on 01/11/2025.
 This is supposed to be decommissionned later, but the replacement is not yet available as of writing.
 """
dataset = "sis-energy-derived-reanalysis"
request = {
    "variable": ["surface_downwelling_shortwave_radiation"],
    "spatial_aggregation": ["original_grid"],
    "temporal_aggregation": ["hourly"],
    "year": ["2025"],
    "month": ["02","03","04","05","06","07","08","09"],
    "spatial_resolution": ["0_25_degree"],
    "area": [48, 0, 47, 0.75]

}



client = cdsapi.Client()
filename = client.retrieve(dataset, request).download()
print(f"Downloaded file: {filename}")

with zipfile.ZipFile(filename, 'r') as zip_ref:
    zip_ref.extractall(target_folder)
