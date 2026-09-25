"""
Download Sentinel-1 SAR & Sentinel-2 MSI data into data/sentinel1_sar/ and data/sentinel2_msi/
Official Source: ESA Copernicus Data Space
Register at: https://dataspace.copernicus.eu
"""
from sentinelsat import SentinelAPI
import os

os.makedirs("data/sentinel1_sar", exist_ok=True)
os.makedirs("data/sentinel2_msi", exist_ok=True)

USER = "YOUR_COPERNICUS_USERNAME"
PASSWORD = "YOUR_COPERNICUS_PASSWORD"

api = SentinelAPI(USER, PASSWORD, 'https://dataspace.copernicus.eu/odata/v1')

# Define Area of Interest as WKT polygon (adjust to your canal command area)
AOI = 'POLYGON((74.0 16.0, 80.0 16.0, 80.0 22.0, 74.0 22.0, 74.0 16.0))'

# --- Sentinel-2 MSI Level-2A ---
print("Searching Sentinel-2 MSI...")
s2_products = api.query(
    area=AOI,
    date=('20230601', '20231031'),
    platformname='Sentinel-2',
    producttype='S2MSI2A',
    cloudcoverpercentage=(0, 30)
)
print(f"Found {len(s2_products)} Sentinel-2 products")
api.download_all(s2_products, directory_path='data/sentinel2_msi/')

# --- Sentinel-1 SAR GRD ---
print("Searching Sentinel-1 SAR GRD...")
s1_products = api.query(
    area=AOI,
    date=('20230601', '20231031'),
    platformname='Sentinel-1',
    producttype='GRD',
    sensoroperationalmode='IW',
    polarisationmode='VV VH'
)
print(f"Found {len(s1_products)} Sentinel-1 products")
api.download_all(s1_products, directory_path='data/sentinel1_sar/')

print("Download complete!")
print("  Sentinel-2 -> data/sentinel2_msi/")
print("  Sentinel-1 -> data/sentinel1_sar/")
