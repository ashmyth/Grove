"""
Download ERA5-Land meteorological data into data/era5_land/
Official Source: ECMWF Copernicus Climate Data Store (CDS)
Register at: https://cds.climate.copernicus.eu
Setup API key: https://cds.climate.copernicus.eu/api-how-to
"""
import cdsapi
import os

os.makedirs("data/era5_land", exist_ok=True)

c = cdsapi.Client()
c.retrieve(
    'reanalysis-era5-land',
    {
        'variable': [
            '2m_temperature',
            'total_precipitation',
            'surface_solar_radiation_downwards',
        ],
        'year': '2023',
        'month': ['06', '07', '08', '09', '10'],
        'day': [f'{d:02d}' for d in range(1, 32)],
        'time': '12:00',
        'format': 'netcdf',
        'area': [22, 74, 16, 80],  # Adjust AOI: [North, West, South, East]
    },
    'data/era5_land/era5_land_kharif2023.nc'
)
print("ERA5-Land download complete -> data/era5_land/era5_land_kharif2023.nc")
