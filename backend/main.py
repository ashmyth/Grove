"""
Grove (GeoPrithvi-Agri) FastAPI Backend Service
Owned by Teammate 3 (API & Web Integration)

Adheres strictly to the Interface 2 and Interface 3 contracts in work-division.md.
Provides realistic mock data for Canal Command Reaches, Parcels, and Multi-temporal Timeseries
so the React dashboard runs seamlessly during parallel development.
"""

from typing import List, Optional, Literal
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

app = FastAPI(
    title="Grove (GeoPrithvi-Agri) API",
    description="Multimodal Remote Sensing & Canal Command Irrigation Deficit Decision Support API",
    version="1.0.0",
)

# Enable CORS for Vite frontend development server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================================================
# Pydantic Schemas (Contract matching architecture.md & work-division.md)
# =====================================================================

class CanalAdvisoryItem(BaseModel):
    id: str
    block_name: str
    reach: Literal["head", "middle", "tail"]
    crop_type: str
    stage: str
    deficit_m3_ha: float
    discharge_cumecs: float
    stress_level: Literal["Normal", "Mild", "Moderate", "Severe"]


class PixelTimeseriesData(BaseModel):
    dates: List[str]
    doy: List[int]
    ndvi_raw: List[float]
    ndvi_smoothed: List[float]
    smi_sar: List[float]
    lst_anomaly: List[float]


class CommandOverview(BaseModel):
    cycle_days: int = 8
    total_area_ha: float
    total_deficit_m3: float
    total_recommended_discharge_cumecs: float
    severe_stress_parcels_count: int
    reaches_count: dict


# =====================================================================
# Synthetic GIS & GeoJSON Data for Mocking
# =====================================================================

MOCK_PARCELS_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "id": "PARCEL-A101",
            "properties": {
                "id": "PARCEL-A101",
                "block_name": "Canal Reach 1A (Head)",
                "reach": "head",
                "crop_type": "Wheat",
                "stage": "Tillering",
                "stress_level": "Normal",
                "stress_score": 0.21,
                "deficit_m3_ha": 35.2,
                "recommended_discharge": 0.35,
                "area_ha": 14.5
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.840, 30.720], [76.852, 30.722], [76.850, 30.710], [76.838, 30.708], [76.840, 30.720]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-B204",
            "properties": {
                "id": "PARCEL-B204",
                "block_name": "Distributary 4 (Middle)",
                "reach": "middle",
                "crop_type": "Mustard",
                "stage": "Flowering",
                "stress_level": "Moderate",
                "stress_score": 0.58,
                "deficit_m3_ha": 142.8,
                "recommended_discharge": 1.25,
                "area_ha": 28.0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.855, 30.715], [76.870, 30.718], [76.868, 30.702], [76.852, 30.700], [76.855, 30.715]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-C309",
            "properties": {
                "id": "PARCEL-C309",
                "block_name": "Tail-End Distributary 9",
                "reach": "tail",
                "crop_type": "Wheat",
                "stage": "Flowering",
                "stress_level": "Severe",
                "stress_score": 0.84,
                "deficit_m3_ha": 265.0,
                "recommended_discharge": 2.45,
                "area_ha": 32.5
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.872, 30.705], [76.890, 30.708], [76.885, 30.690], [76.868, 30.688], [76.872, 30.705]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-C310",
            "properties": {
                "id": "PARCEL-C310",
                "block_name": "Tail-End Distributary 10",
                "reach": "tail",
                "crop_type": "Barley",
                "stage": "Grain Filling",
                "stress_level": "Severe",
                "stress_score": 0.91,
                "deficit_m3_ha": 310.5,
                "recommended_discharge": 2.90,
                "area_ha": 24.0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.892, 30.695], [76.910, 30.698], [76.905, 30.680], [76.888, 30.678], [76.892, 30.695]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-A102",
            "properties": {
                "id": "PARCEL-A102",
                "block_name": "Canal Reach 1B (Head)",
                "reach": "head",
                "crop_type": "Wheat",
                "stage": "Vegetative",
                "stress_level": "Normal",
                "stress_score": 0.18,
                "deficit_m3_ha": 40.0,
                "recommended_discharge": 0.40,
                "area_ha": 18.0
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.835, 30.735], [76.850, 30.738], [76.848, 30.722], [76.832, 30.720], [76.835, 30.735]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-B205",
            "properties": {
                "id": "PARCEL-B205",
                "block_name": "Distributary 5 (Middle)",
                "reach": "middle",
                "crop_type": "Gram",
                "stage": "Pod Development",
                "stress_level": "Mild",
                "stress_score": 0.42,
                "deficit_m3_ha": 85.0,
                "recommended_discharge": 0.75,
                "area_ha": 16.5
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.860, 30.730], [76.875, 30.732], [76.872, 30.718], [76.856, 30.716], [76.860, 30.730]]]
            }
        }
    ]
}

MOCK_CANAL_NETWORK_GEOJSON = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "name": "Main Feeder Branch (Head to Tail)",
                "type": "Main Canal",
                "flow_direction": "SE"
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [76.830, 30.740],
                    [76.845, 30.725],
                    [76.865, 30.710],
                    [76.885, 30.695],
                    [76.915, 30.675]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Distributary Branch 4",
                "type": "Distributary",
                "flow_direction": "SW"
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [76.865, 30.710],
                    [76.855, 30.700],
                    [76.845, 30.690]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "name": "Tail Lateral 9",
                "type": "Lateral",
                "flow_direction": "S"
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [76.885, 30.695],
                    [76.890, 30.680],
                    [76.895, 30.665]
                ]
            }
        }
    ]
}


# =====================================================================
# REST Endpoints
# =====================================================================

@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "grove-backend",
        "model_status": "mock_mode",
        "teammate_fence": "teammate_3_active"
    }


@app.get("/api/v1/overview", response_model=CommandOverview)
def get_command_overview():
    """Returns top-level canal command summary statistics."""
    features = MOCK_PARCELS_GEOJSON["features"]
    total_area = sum(f["properties"]["area_ha"] for f in features)
    total_def = sum(f["properties"]["deficit_m3_ha"] * f["properties"]["area_ha"] for f in features)
    total_disc = sum(f["properties"]["recommended_discharge"] for f in features)
    severe_count = sum(1 for f in features if f["properties"]["stress_level"] == "Severe")
    
    return CommandOverview(
        cycle_days=8,
        total_area_ha=round(total_area, 1),
        total_deficit_m3=round(total_def, 1),
        total_recommended_discharge_cumecs=round(total_disc, 2),
        severe_stress_parcels_count=severe_count,
        reaches_count={"head": 2, "middle": 2, "tail": 2}
    )


@app.get("/api/v1/canal-advisory", response_model=List[CanalAdvisoryItem])
def get_canal_advisory(reach: Optional[str] = None, stress: Optional[str] = None):
    """
    Returns canal discharge advisory items across all reaches.
    Filterable by reach ('head', 'middle', 'tail') or stress level.
    """
    items = []
    for f in MOCK_PARCELS_GEOJSON["features"]:
        p = f["properties"]
        if reach and p["reach"].lower() != reach.lower():
            continue
        if stress and p["stress_level"].lower() != stress.lower():
            continue
        items.append(
            CanalAdvisoryItem(
                id=p["id"],
                block_name=p["block_name"],
                reach=p["reach"],
                crop_type=p["crop_type"],
                stage=p["stage"],
                deficit_m3_ha=p["deficit_m3_ha"],
                discharge_cumecs=p["recommended_discharge"],
                stress_level=p["stress_level"]
            )
        )
    return items


@app.get("/api/v1/parcels/geojson")
def get_parcels_geojson():
    """Returns GeoJSON FeatureCollection of command parcels with stress attributes."""
    return MOCK_PARCELS_GEOJSON


@app.get("/api/v1/canal/network")
def get_canal_network():
    """Returns GeoJSON FeatureCollection of canal line networks."""
    return MOCK_CANAL_NETWORK_GEOJSON


@app.get("/api/v1/pixel-timeseries", response_model=PixelTimeseriesData)
def get_pixel_timeseries(
    parcel_id: Optional[str] = Query(default="PARCEL-C309"),
    lat: Optional[float] = None,
    lon: Optional[float] = None
):
    """
    Returns multi-temporal DOY curve with raw vs Savitzky-Golay smoothed NDVI,
    SAR SMI soil moisture index, and LST anomalies.
    """
    # Realistic 8-point 12-day cadence winter rabi season (DOY 330 to 75)
    dates = ["2026-11-25", "2026-12-07", "2026-12-19", "2026-12-31", "2027-01-12", "2027-01-24", "2027-02-05", "2027-02-17"]
    doy = [329, 341, 353, 365, 12, 24, 36, 48]
    
    # Stress curves vary slightly based on parcel
    if parcel_id and "C3" in parcel_id:  # Tail end stress (dropping NDVI, plummeting SMI)
        ndvi_raw = [0.24, 0.38, 0.52, 0.61, 0.58, 0.54, 0.49, 0.43]
        ndvi_smoothed = [0.25, 0.37, 0.51, 0.60, 0.57, 0.53, 0.48, 0.42]
        smi_sar = [0.65, 0.55, 0.42, 0.31, 0.22, 0.18, 0.15, 0.12]
        lst_anomaly = [-0.5, 0.2, 0.8, 1.4, 2.3, 3.1, 3.8, 4.2]
    else:  # Head or middle healthy
        ndvi_raw = [0.22, 0.36, 0.54, 0.68, 0.76, 0.81, 0.79, 0.75]
        ndvi_smoothed = [0.23, 0.35, 0.53, 0.67, 0.75, 0.80, 0.78, 0.74]
        smi_sar = [0.72, 0.68, 0.65, 0.61, 0.59, 0.55, 0.52, 0.49]
        lst_anomaly = [-0.8, -0.4, 0.1, 0.2, 0.4, 0.3, 0.5, 0.6]

    return PixelTimeseriesData(
        dates=dates,
        doy=doy,
        ndvi_raw=ndvi_raw,
        ndvi_smoothed=ndvi_smoothed,
        smi_sar=smi_sar,
        lst_anomaly=lst_anomaly
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
