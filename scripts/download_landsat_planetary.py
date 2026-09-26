import pystac_client
import planetary_computer
import requests
import os

# Create the folder if it doesn't exist
os.makedirs("data/landsat89_modis", exist_ok=True)

print("Connecting to Microsoft Planetary Computer...")
catalog = pystac_client.Client.open(
    "https://planetarycomputer.microsoft.com/api/stac/v1",
    modifier=planetary_computer.sign_inplace,
)

# This is the exact ID from your screenshot!
item_id = "LC08_L2SP_144053_20260908_02_T1"
print(f"Searching for {item_id}...")

search = catalog.search(
    collections=["landsat-c2-l2"],
    ids=[item_id]
)

items = list(search.items())
if not items:
    print("Item not found!")
    exit()

item = items[0]

# We will download the crucial bands for agriculture (Red, Near-Infrared, and Thermal)
assets_to_download = {
    "red": "Band_4_Red",
    "nir08": "Band_5_NIR", 
    "lwir11": "Band_10_Thermal"
}

for stac_key, human_name in assets_to_download.items():
    if stac_key in item.assets:
        url = item.assets[stac_key].href
        filename = f"data/landsat89_modis/{item_id}_{human_name}.tif"
        
        print(f"Downloading {human_name} ({stac_key})...")
        response = requests.get(url, stream=True)
        with open(filename, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"Saved: {filename}")

print("\nSuccess! All files downloaded to data/landsat89_modis/")
