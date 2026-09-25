"""
Synthetic GeoTIFF Generator for Grove (GeoPrithvi-Agri)
Generates lightweight 12-channel 10m metric-aligned GeoTIFF composite chips
for offline ML model testing and data loader verification.
"""

import os
import sys
import numpy as np

def create_synthetic_geotiff(output_path: str, height: int = 224, width: int = 224):
    """
    Creates a 12-channel 224x224 synthetic GeoTIFF composite chip.
    Channels:
      1: B2 (Blue)
      2: B3 (Green)
      3: B4 (Red)
      4: B8 (NIR)
      5: B11 (SWIR1)
      6: B12 (SWIR2)
      7: VV (Sentinel-1 SAR dB)
      8: VH (Sentinel-1 SAR dB)
      9: LST (Land Surface Temp deg C)
      10: DEM (Elevation m)
      11: Slope (Degrees)
      12: SCL (Scene Classification Layer)
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    try:
        import rasterio
        from rasterio.transform import from_origin
        
        # Spatial metadata: Centered around Kuttanad / Canal Command (EPSG:32643 UTM Zone 43N or WGS84 EPSG:4326)
        transform = from_origin(76.40, 9.55, 0.0001, 0.0001)  # ~10m resolution in deg
        
        # Create synthetic data with realistic spectral/SAR profiles
        np.random.seed(42)
        
        data = np.zeros((12, height, width), dtype=np.float32)
        
        # Optical reflectance (0.0 to 1.0)
        data[0] = np.random.uniform(0.02, 0.08, (height, width))  # B2
        data[1] = np.random.uniform(0.04, 0.12, (height, width))  # B3
        data[2] = np.random.uniform(0.03, 0.15, (height, width))  # B4
        data[3] = np.random.uniform(0.25, 0.55, (height, width))  # B8 (NIR high for vegetation)
        data[4] = np.random.uniform(0.10, 0.30, (height, width))  # B11
        data[5] = np.random.uniform(0.05, 0.20, (height, width))  # B12
        
        # SAR backscatter (dB -25 to 0)
        data[6] = np.random.uniform(-15.0, -5.0, (height, width))   # VV
        data[7] = np.random.uniform(-22.0, -10.0, (height, width))  # VH
        
        # Thermal LST (deg C)
        data[8] = np.random.uniform(26.0, 36.0, (height, width))
        
        # DEM & Slope
        data[9] = np.random.uniform(5.0, 45.0, (height, width))
        data[10] = np.random.uniform(0.0, 8.0, (height, width))
        
        # SCL (4=Vegetation, 5=Bare Soil, 6=Water, 8=Cloud)
        scl = np.full((height, width), 4, dtype=np.float32)
        scl[0:20, 0:20] = 8.0  # mock small cloud patch in corner
        data[11] = scl
        
        profile = {
            'driver': 'GTiff',
            'height': height,
            'width': width,
            'count': 12,
            'dtype': 'float32',
            'crs': 'EPSG:4326',
            'transform': transform,
            'compress': 'lzw'
        }
        
        with rasterio.open(output_path, 'w', **profile) as dst:
            for band_idx in range(12):
                dst.write(data[band_idx], band_idx + 1)
                
        print(f"Created 12-channel GeoTIFF at: {output_path}")
        return True
        
    except ImportError:
        # Fallback to NumPy npz/npy or basic binary header if rasterio not installed yet
        print("Rasterio not available yet; writing synthetic raw binary chip.")
        np_data = np.random.randn(12, height, width).astype(np.float32)
        np.save(output_path.replace('.tif', '.npy'), np_data)
        return False

if __name__ == '__main__':
    target = os.path.join(os.path.dirname(__file__), '..', 'data', 'sample_chip.tif')
    create_synthetic_geotiff(os.path.abspath(target))
