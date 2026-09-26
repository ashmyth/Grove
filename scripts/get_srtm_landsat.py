"""
Download SRTM DEM & Landsat-8 TIRS Band 10 into data/srtm_dem/ and data/landsat8_tirs/
Official Source: USGS EarthExplorer
Register at: https://earthexplorer.usgs.gov
"""
import elevation
import os

# --- SRTM DEM ---
os.makedirs("data/srtm_dem", exist_ok=True)
print("Downloading SRTM DEM...")
# Adjust bounds to your AOI: (lon_min, lat_min, lon_max, lat_max)
elevation.clip(bounds=(74.0, 16.0, 80.0, 22.0), output='data/srtm_dem/srtm_aoi.tif')
elevation.clean()
print("SRTM DEM download complete -> data/srtm_dem/srtm_aoi.tif")

# --- Landsat-8 TIRS Band 10 ---
os.makedirs("data/landsat8_tirs", exist_ok=True)
try:
    from landsatxplore.earthexplorer import EarthExplorer
    USER = "YOUR_USGS_USERNAME"
    PASSWORD = "YOUR_USGS_PASSWORD"

    print("Searching Landsat-8 TIRS scenes...")
    ee = EarthExplorer(USER, PASSWORD)
    scenes = ee.search(
        dataset='landsat_ot_c2_l2',
        bbox=[74.0, 16.0, 80.0, 22.0],
        start_date='2023-06-01',
        end_date='2023-10-31',
        max_cloud_cover=20
    )
    print(f"Found {len(scenes)} Landsat-8 scenes")
    for scene in scenes[:5]:
        ee.download(scene['landsat_product_id'], output_dir='data/landsat8_tirs/')
    ee.logout()
    print("Landsat-8 TIRS download complete -> data/landsat8_tirs/")
except ImportError:
    print("Install landsatxplore: pip install landsatxplore")
