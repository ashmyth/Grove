# Dataset Sources & Download Guide — Grove (GeoPrithvi-Agri)

All datasets must be saved in their respective subdirectories inside this `dataset/` folder.

---

## 📁 Folder Structure

```
dataset/
├── sentinel2_msi/               # Sentinel-2 Optical (ESA Copernicus)
├── sentinel1_sar/               # Sentinel-1 SAR (ESA Copernicus)
├── era5_land/                   # ERA5-Land Meteorological Reanalysis (ECMWF)
├── canal_shapefiles/            # Canal Command Area Shapefiles (India WRIS)
├── landsat8_tirs/               # Landsat-8 TIRS Band 10 Thermal (USGS)
├── srtm_dem/                    # SRTM Digital Elevation Model (NASA/USGS)
├── prithvi_crop_classification/ # IBM-NASA Prithvi HLS Crop Dataset (HuggingFace)
├── cirad_geode/                 # CIRAD GeoDE Agricultural Datasets
├── isro_liss_awifs/             # ISRO LISS-III / AWiFS / EOS-04 SAR (NRSC Bhuvan)
└── landsat89_modis/             # Landsat-8/9 OLI & MODIS (USGS/NASA Earthdata)
```

---

## 1. 🛰️ Sentinel-2 MSI (Optical Multispectral)

| | |
|---|---|
| **Official Source** | ESA Copernicus Data Space |
| **URL** | https://dataspace.copernicus.eu |
| **Product** | `S2MSI2A` (Level-2A Surface Reflectance) |
| **Resolution** | 10m – 20m |
| **Access** | Free (Registration required) |
| **Save to** | `dataset/sentinel2_msi/` |

**Download Steps:**
1. Register at https://dataspace.copernicus.eu
2. Use the browser to search by Area of Interest (your canal command polygon)
3. Filter: Collection = `SENTINEL-2`, Product Type = `S2MSI2A`
4. Download `.zip` and extract into `dataset/sentinel2_msi/`

**OR via Python (`sentinelsat`):**
```bash
pip install sentinelsat
```
```python
from sentinelsat import SentinelAPI
api = SentinelAPI('YOUR_USER', 'YOUR_PASSWORD', 'https://dataspace.copernicus.eu/odata/v1')
products = api.query(area='POLYGON((...))', date=('20230601', '20231001'), platformname='Sentinel-2', producttype='S2MSI2A')
api.download_all(products, directory_path='dataset/sentinel2_msi/')
```

---

## 2. 📡 Sentinel-1 C-Band SAR (GRD)

| | |
|---|---|
| **Official Source** | ESA Copernicus Data Space |
| **URL** | https://dataspace.copernicus.eu |
| **Product** | `GRD` (Ground Range Detected, IW mode, VV+VH) |
| **Resolution** | 10m |
| **Access** | Free (Registration required) |
| **Save to** | `dataset/sentinel1_sar/` |

**Download Steps:**
1. Login at https://dataspace.copernicus.eu
2. Filter: Collection = `SENTINEL-1`, Product Type = `GRD`, Instrument Mode = `IW`
3. Download and extract into `dataset/sentinel1_sar/`

**Alaska SAR Facility (Alternative):**
- URL: https://search.asf.alaska.edu
- Search for Sentinel-1 GRD IW products

---

## 3. 🌤️ ERA5-Land Reanalysis (Meteorological)

| | |
|---|---|
| **Official Source** | ECMWF Copernicus Climate Data Store (CDS) |
| **URL** | https://cds.climate.copernicus.eu |
| **Variables** | `2m_temperature`, `total_precipitation`, `surface_solar_radiation_downwards` |
| **Resolution** | 0.1° (~9km) |
| **Access** | Free (Registration + API key required) |
| **Save to** | `dataset/era5_land/` |

**Download via Python (`cdsapi`):**
```bash
pip install cdsapi
```
```python
import cdsapi
c = cdsapi.Client()
c.retrieve('reanalysis-era5-land', {
    'variable': ['2m_temperature', 'total_precipitation', 'surface_solar_radiation_downwards'],
    'year': '2023', 'month': ['06', '07', '08', '09', '10'],
    'day': [f'{d:02d}' for d in range(1,32)],
    'time': '12:00',
    'format': 'netcdf',
    'area': [22, 74, 16, 80],  # North, West, South, East — adjust to your AOI
}, 'dataset/era5_land/era5_land_kharif2023.nc')
```

---

## 4. 🗺️ Canal Command Area Shapefiles

| | |
|---|---|
| **Official Source** | India Water Resources Information System (WRIS) |
| **URL** | https://indiawris.gov.in |
| **Format** | Shapefile (.shp, .dbf, .shx) or GeoJSON |
| **Access** | Free (Registration required) |
| **Save to** | `dataset/canal_shapefiles/` |

**Download Steps:**
1. Visit https://indiawris.gov.in/wris/#/
2. Navigate to **GIS Data → River Basins / Canal Networks**
3. Select your specific canal command area / river basin
4. Export as Shapefile and save to `dataset/canal_shapefiles/`

**Alternative (OPEN GOVERNMENT DATA):**
- URL: https://data.gov.in
- Search for "canal command area shapefile"

---

## 5. 🌡️ Landsat-8 TIRS Band 10 (Thermal Infrared)

| | |
|---|---|
| **Official Source** | USGS EarthExplorer |
| **URL** | https://earthexplorer.usgs.gov |
| **Product** | `Landsat Collection 2 Level-2` (LC08_L2SP) |
| **Band** | Band 10 (TIRS1, 10.6–11.19 μm) |
| **Resolution** | 30m (resampled to 100m) |
| **Access** | Free (USGS registration required) |
| **Save to** | `dataset/landsat8_tirs/` |

**Download via Python (`landsatxplore`):**
```bash
pip install landsatxplore
```
```python
from landsatxplore.earthexplorer import EarthExplorer
ee = EarthExplorer('YOUR_USERNAME', 'YOUR_PASSWORD')
scenes = ee.search(dataset='landsat_ot_c2_l2', bbox=[74, 16, 80, 22],
                   start_date='2023-06-01', end_date='2023-10-31', max_cloud_cover=20)
for scene in scenes[:5]:
    ee.download(scene['landsat_product_id'], output_dir='dataset/landsat8_tirs/')
ee.logout()
```

---

## 6. 🏔️ SRTM Digital Elevation Model

| | |
|---|---|
| **Official Source** | NASA / USGS EarthExplorer |
| **URL** | https://earthexplorer.usgs.gov OR https://srtm.csi.cgiar.org |
| **Product** | SRTM 1 Arc-Second Global (~30m) |
| **Format** | GeoTIFF |
| **Access** | Free |
| **Save to** | `dataset/srtm_dem/` |

**Download via Python (`elevation` library):**
```bash
pip install elevation
```
```python
import elevation
# Clip to your area of interest (lon_min, lat_min, lon_max, lat_max)
elevation.clip(bounds=(74.0, 16.0, 80.0, 22.0), output='dataset/srtm_dem/srtm_aoi.tif')
elevation.clean()
```

---

## 7. 🧠 IBM-NASA Prithvi Crop Classification Dataset

| | |
|---|---|
| **Official Source** | Hugging Face Hub |
| **URL** | https://huggingface.co/datasets/ibm-nasa-geospatial/multi-temporal-crop-classification |
| **Contents** | 224×224 px HLS chips, 18 bands (6 bands × 3 time-steps), CDL labels |
| **Access** | Free |
| **Save to** | `dataset/prithvi_crop_classification/` |

**Download via Git LFS:**
```bash
git lfs install
git clone https://huggingface.co/datasets/ibm-nasa-geospatial/multi-temporal-crop-classification dataset/prithvi_crop_classification/
```

**OR via Python:**
```python
from datasets import load_dataset
ds = load_dataset("ibm-nasa-geospatial/multi-temporal-crop-classification", cache_dir="dataset/prithvi_crop_classification/")
```

---

## 8. 🌾 CIRAD GeoDE Agricultural Datasets

| | |
|---|---|
| **Official Source** | CIRAD GeoDE Geospatial Data Portal |
| **URL** | https://geode.cirad.fr |
| **Contents** | Tropical land use, crop mapping, agricultural boundary datasets |
| **Access** | Free (Browse catalog and download per dataset) |
| **Save to** | `dataset/cirad_geode/` |

**Download Steps:**
1. Visit https://geode.cirad.fr
2. Search for relevant crop/agriculture datasets for your AOI
3. Download data files (GeoTIFF / Shapefile) and save to `dataset/cirad_geode/`

---

## 9. 🇮🇳 ISRO LISS-III / AWiFS & EOS-04 (RISAT-1A SAR)

| | |
|---|---|
| **Official Source** | NRSC Bhoonidhi / Bhuvan |
| **Bhuvan URL** | https://bhuvan.nrsc.gov.in |
| **Bhoonidhi URL** | https://bhoonidhi.nrsc.gov.in |
| **Sensors** | LISS-III (23.5m), AWiFS (56m), EOS-04 C-Band SAR |
| **Access** | Free (NRSC registration required) |
| **Save to** | `dataset/isro_liss_awifs/` |

**Download Steps:**
1. Register at https://bhoonidhi.nrsc.gov.in
2. Search by Satellite/Sensor: `Resourcesat-2A/LISS-III`, `Resourcesat-2/AWiFS`, or `EOS-04` (for SAR)
3. Draw your Area of Interest on the map
4. Add scenes to cart and download
5. Extract and save to `dataset/isro_liss_awifs/`

---

## 10. 🌍 Landsat-8/9 OLI & MODIS

| | |
|---|---|
| **Official Source (Landsat)** | USGS EarthExplorer |
| **Official Source (MODIS)** | NASA Earthdata (LAADS DAAC) |
| **Landsat URL** | https://earthexplorer.usgs.gov |
| **MODIS URL** | https://ladsweb.modaps.eosdis.nasa.gov |
| **Products** | `LC08/LC09 Collection 2 L2`, `MOD09A1` (MODIS 8-day Surface Reflectance) |
| **Access** | Free (registration required) |
| **Save to** | `dataset/landsat89_modis/` |

**Download MODIS via Python (`pymodis`):**
```bash
pip install pymodis
```
```python
from pymodis import downmodis
downer = downmodis.downModis(
    destinationFolder='dataset/landsat89_modis/',
    product='MOD09A1.061',
    tiles='h24v07',  # Adjust tile for your AOI
    today='2023-10-01',
    enddate='2023-06-01',
    user='YOUR_EARTHDATA_USERNAME',
    password='YOUR_EARTHDATA_PASSWORD'
)
downer.connect()
downer.downloadsAllDay()
```

---

## ⚠️ Important Notes

> **Large File Sizes:** These datasets can be very large (GBs to TBs). It is recommended to download only the specific Area of Interest (AOI) and date range needed for the project.

> **`.gitignore`:** The `dataset/` folder is (or should be) added to `.gitignore` so raw data is NOT pushed to GitHub. Only the folder structure with `README.md` is committed.

> **Credentials Required:** ERA5 (CDS API key), Copernicus (free account), USGS (free account), NASA Earthdata (free account), and NRSC Bhoonidhi (free account) registrations are all needed.
