"""
Grove (GeoPrithvi-Agri) - High-Fidelity Agricultural GIS Datasets
Provides realistic canal network geometries, agricultural field parcels, and multi-sensor telemetry
for Sirhind Canal Command (Punjab) and Kuttanad Canal Command (Kerala).
"""

import json
from pathlib import Path
from typing import Dict, Any, Tuple

DATA_DIR = Path(__file__).resolve().parent.parent / "data"

# ==============================================================================
# 1. SIRHIND CANAL COMMAND (PUNJAB, INDIA) - ALLUVIAL AGRICULTURAL PLAINS
# Center: 30.638° N, 76.385° E (Fatehgarh Sahib / Sirhind agricultural basin)
# ==============================================================================

SIRHIND_CANAL_NETWORK: Dict[str, Any] = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "properties": {
                "id": "CANAL-MAIN-01",
                "name": "Sirhind Main Feeder Canal (Head to Tail)",
                "type": "Main Canal",
                "flow_direction": "SW",
                "capacity_cumecs": 45.0,
                "length_km": 14.2
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [76.345, 30.668],
                    [76.365, 30.655],
                    [76.385, 30.640],
                    [76.405, 30.622],
                    [76.428, 30.605]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "id": "CANAL-DIST-1N",
                "name": "Head Reach Distributary 1 (North)",
                "type": "Distributary",
                "flow_direction": "NW",
                "capacity_cumecs": 14.5,
                "length_km": 6.8
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [76.365, 30.655],
                    [76.360, 30.672],
                    [76.352, 30.686]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "id": "CANAL-DIST-2S",
                "name": "Middle Reach Distributary 2 (South)",
                "type": "Distributary",
                "flow_direction": "SE",
                "capacity_cumecs": 12.0,
                "length_km": 7.4
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [76.385, 30.640],
                    [76.398, 30.630],
                    [76.412, 30.615]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "id": "CANAL-LAT-9T",
                "name": "Tail-End Lateral Branch 9",
                "type": "Lateral",
                "flow_direction": "S",
                "capacity_cumecs": 6.5,
                "length_km": 5.1
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [76.405, 30.622],
                    [76.418, 30.612],
                    [76.430, 30.598]
                ]
            }
        },
        {
            "type": "Feature",
            "properties": {
                "id": "CANAL-MIN-10T",
                "name": "Tail Terminal Minor 10",
                "type": "Minor",
                "flow_direction": "SW",
                "capacity_cumecs": 3.8,
                "length_km": 4.5
            },
            "geometry": {
                "type": "LineString",
                "coordinates": [
                    [76.428, 30.605],
                    [76.440, 30.592],
                    [76.452, 30.578]
                ]
            }
        }
    ]
}

SIRHIND_PARCELS_GEOJSON: Dict[str, Any] = {
    "type": "FeatureCollection",
    "features": [
        # --- HEAD REACH (WELL-IRRIGATED / LOW DEFICIT / GREEN) ---
        {
            "type": "Feature",
            "id": "PARCEL-H101",
            "properties": {
                "id": "PARCEL-H101",
                "block_name": "Canal Reach 1A (Head Intake)",
                "reach": "head",
                "crop_type": "Wheat (PBW-824)",
                "stage": "Tillering",
                "stress_level": "Normal",
                "stress_score": 0.16,
                "ndvi": 0.78,
                "smi_sar": 0.72,
                "lst_anomaly": -0.8,
                "deficit_m3_ha": 32.5,
                "recommended_discharge": 0.35,
                "area_ha": 18.5,
                "farmer": "Gurpreet Singh (Chak 12)"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.348, 30.672], [76.362, 30.672], [76.362, 30.660], [76.348, 30.660], [76.348, 30.672]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-H102",
            "properties": {
                "id": "PARCEL-H102",
                "block_name": "Canal Reach 1B (Head Intake)",
                "reach": "head",
                "crop_type": "Mustard (Pusa Bold)",
                "stage": "Vegetative",
                "stress_level": "Normal",
                "stress_score": 0.19,
                "ndvi": 0.74,
                "smi_sar": 0.68,
                "lst_anomaly": -0.5,
                "deficit_m3_ha": 38.0,
                "recommended_discharge": 0.40,
                "area_ha": 14.2,
                "farmer": "Jaswant Gill (Chak 14)"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.363, 30.672], [76.376, 30.672], [76.376, 30.660], [76.363, 30.660], [76.363, 30.672]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-H103",
            "properties": {
                "id": "PARCEL-H103",
                "block_name": "Distributary 1-North Block",
                "reach": "head",
                "crop_type": "Wheat (HD-3086)",
                "stage": "Crown Root Initiation",
                "stress_level": "Normal",
                "stress_score": 0.22,
                "ndvi": 0.81,
                "smi_sar": 0.75,
                "lst_anomaly": -0.7,
                "deficit_m3_ha": 42.0,
                "recommended_discharge": 0.45,
                "area_ha": 22.0,
                "farmer": "Harmanpreet Mann"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.345, 30.688], [76.358, 30.688], [76.358, 30.675], [76.345, 30.675], [76.345, 30.688]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-H104",
            "properties": {
                "id": "PARCEL-H104",
                "block_name": "Distributary 1-North Block",
                "reach": "head",
                "crop_type": "Sugarcane (Co-0238)",
                "stage": "Tillering",
                "stress_level": "Normal",
                "stress_score": 0.24,
                "ndvi": 0.83,
                "smi_sar": 0.71,
                "lst_anomaly": -0.4,
                "deficit_m3_ha": 45.5,
                "recommended_discharge": 0.50,
                "area_ha": 26.5,
                "farmer": "Balwinder Dhillon"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.359, 30.688], [76.372, 30.688], [76.372, 30.675], [76.359, 30.675], [76.359, 30.688]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-H105",
            "properties": {
                "id": "PARCEL-H105",
                "block_name": "Head Feeder South Polder",
                "reach": "head",
                "crop_type": "Wheat (PBW-824)",
                "stage": "Tillering",
                "stress_level": "Normal",
                "stress_score": 0.18,
                "ndvi": 0.79,
                "smi_sar": 0.70,
                "lst_anomaly": -0.6,
                "deficit_m3_ha": 36.0,
                "recommended_discharge": 0.38,
                "area_ha": 16.8,
                "farmer": "Amarjit Sandhu"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.352, 30.658], [76.368, 30.658], [76.368, 30.645], [76.352, 30.645], [76.352, 30.658]]]
            }
        },

        # --- MIDDLE REACH (MODERATE STRESS / TRANSITIONAL / AMBER-YELLOW) ---
        {
            "type": "Feature",
            "id": "PARCEL-M201",
            "properties": {
                "id": "PARCEL-M201",
                "block_name": "Distributary 2 (Middle Reach)",
                "reach": "middle",
                "crop_type": "Wheat (HD-3086)",
                "stage": "Stem Elongation",
                "stress_level": "Mild",
                "stress_score": 0.38,
                "ndvi": 0.64,
                "smi_sar": 0.52,
                "lst_anomaly": 0.6,
                "deficit_m3_ha": 82.0,
                "recommended_discharge": 0.85,
                "area_ha": 19.5,
                "farmer": "Kuldeep Brar"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.372, 30.654], [76.386, 30.654], [76.386, 30.642], [76.372, 30.642], [76.372, 30.654]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-M202",
            "properties": {
                "id": "PARCEL-M202",
                "block_name": "Distributary 2 (Middle Reach)",
                "reach": "middle",
                "crop_type": "Cotton (Bt-RCH)",
                "stage": "Boll Formation",
                "stress_level": "Moderate",
                "stress_score": 0.56,
                "ndvi": 0.58,
                "smi_sar": 0.44,
                "lst_anomaly": 1.4,
                "deficit_m3_ha": 128.0,
                "recommended_discharge": 1.20,
                "area_ha": 24.0,
                "farmer": "Navtej Cheema"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.387, 30.654], [76.402, 30.654], [76.402, 30.642], [76.387, 30.642], [76.387, 30.654]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-M203",
            "properties": {
                "id": "PARCEL-M203",
                "block_name": "Central Branch Minor 4",
                "reach": "middle",
                "crop_type": "Maize (PMH-1)",
                "stage": "Flowering",
                "stress_level": "Moderate",
                "stress_score": 0.61,
                "ndvi": 0.55,
                "smi_sar": 0.41,
                "lst_anomaly": 1.8,
                "deficit_m3_ha": 142.5,
                "recommended_discharge": 1.35,
                "area_ha": 21.0,
                "farmer": "Manjit Virk"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.375, 30.640], [76.390, 30.640], [76.390, 30.628], [76.375, 30.628], [76.375, 30.640]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-M204",
            "properties": {
                "id": "PARCEL-M204",
                "block_name": "Central Branch Minor 4",
                "reach": "middle",
                "crop_type": "Mustard (Pusa Bold)",
                "stage": "Flowering",
                "stress_level": "Mild",
                "stress_score": 0.44,
                "ndvi": 0.61,
                "smi_sar": 0.48,
                "lst_anomaly": 0.9,
                "deficit_m3_ha": 96.0,
                "recommended_discharge": 0.95,
                "area_ha": 17.5,
                "farmer": "Sukhwinder Aulakh"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.391, 30.638], [76.406, 30.638], [76.406, 30.626], [76.391, 30.626], [76.391, 30.638]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-M205",
            "properties": {
                "id": "PARCEL-M205",
                "block_name": "Middle Feeder Basin West",
                "reach": "middle",
                "crop_type": "Gram / Chickpea",
                "stage": "Pod Development",
                "stress_level": "Moderate",
                "stress_score": 0.59,
                "ndvi": 0.56,
                "smi_sar": 0.43,
                "lst_anomaly": 1.5,
                "deficit_m3_ha": 134.0,
                "recommended_discharge": 1.25,
                "area_ha": 15.0,
                "farmer": "Paramjit Sidhu"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.388, 30.625], [76.402, 30.625], [76.402, 30.612], [76.388, 30.612], [76.388, 30.625]]]
            }
        },

        # --- TAIL REACH (ACUTE WATER STARVATION / SEVERE DEFICIT / CRIMSON RED) ---
        {
            "type": "Feature",
            "id": "PARCEL-T301",
            "properties": {
                "id": "PARCEL-T301",
                "block_name": "Tail-End Distributary 9A",
                "reach": "tail",
                "crop_type": "Wheat (PBW-725)",
                "stage": "Flowering / Heading",
                "stress_level": "Severe",
                "stress_score": 0.85,
                "ndvi": 0.42,
                "smi_sar": 0.19,
                "lst_anomaly": 3.4,
                "deficit_m3_ha": 268.0,
                "recommended_discharge": 2.50,
                "area_ha": 28.5,
                "farmer": "Daljit Dhillon (Tail Sector)"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.404, 30.620], [76.418, 30.620], [76.418, 30.608], [76.404, 30.608], [76.404, 30.620]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-T302",
            "properties": {
                "id": "PARCEL-T302",
                "block_name": "Tail-End Distributary 9B",
                "reach": "tail",
                "crop_type": "Barley (DWRB-137)",
                "stage": "Grain Filling",
                "stress_level": "Severe",
                "stress_score": 0.92,
                "ndvi": 0.37,
                "smi_sar": 0.14,
                "lst_anomaly": 4.2,
                "deficit_m3_ha": 315.0,
                "recommended_discharge": 2.95,
                "area_ha": 22.0,
                "farmer": "Rajinder Bajwa"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.419, 30.618], [76.434, 30.618], [76.434, 30.605], [76.419, 30.605], [76.419, 30.618]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-T303",
            "properties": {
                "id": "PARCEL-T303",
                "block_name": "Tail Terminal Minor 10",
                "reach": "tail",
                "crop_type": "Wheat (PBW-824)",
                "stage": "Flowering / Heading",
                "stress_level": "Severe",
                "stress_score": 0.88,
                "ndvi": 0.39,
                "smi_sar": 0.16,
                "lst_anomaly": 3.8,
                "deficit_m3_ha": 285.0,
                "recommended_discharge": 2.70,
                "area_ha": 25.0,
                "farmer": "Harjinder Toor"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.410, 30.604], [76.425, 30.604], [76.425, 30.592], [76.410, 30.592], [76.410, 30.604]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-T304",
            "properties": {
                "id": "PARCEL-T304",
                "block_name": "Tail Terminal Minor 10",
                "reach": "tail",
                "crop_type": "Gram / Chickpea",
                "stage": "Pod Development",
                "stress_level": "Severe",
                "stress_score": 0.81,
                "ndvi": 0.44,
                "smi_sar": 0.21,
                "lst_anomaly": 2.9,
                "deficit_m3_ha": 242.0,
                "recommended_discharge": 2.30,
                "area_ha": 18.0,
                "farmer": "Avtar Sandhu"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.426, 30.602], [76.442, 30.602], [76.442, 30.590], [76.426, 30.590], [76.426, 30.602]]]
            }
        },
        {
            "type": "Feature",
            "id": "PARCEL-T305",
            "properties": {
                "id": "PARCEL-T305",
                "block_name": "Far Tail Lateral 11 (Outfall)",
                "reach": "tail",
                "crop_type": "Wheat (Late Sown)",
                "stage": "Stem Elongation",
                "stress_level": "Severe",
                "stress_score": 0.94,
                "ndvi": 0.34,
                "smi_sar": 0.12,
                "lst_anomaly": 4.5,
                "deficit_m3_ha": 335.0,
                "recommended_discharge": 3.10,
                "area_ha": 30.0,
                "farmer": "Jagtar Mahal"
            },
            "geometry": {
                "type": "Polygon",
                "coordinates": [[[76.435, 30.588], [76.452, 30.588], [76.452, 30.575], [76.435, 30.575], [76.435, 30.588]]]
            }
        }
    ]
}


# ==============================================================================
# 2. KUTTANAD CANAL COMMAND (ALAPPUZHA, KERALA) - WETLAND POLDERS
# Center: 9.50° N, 76.43° E (AC Canal / Vembanad Wetland Command)
# Loaded dynamically from data/sample_parcels.geojson & canal_command_boundary.geojson
# ==============================================================================

def load_kuttanad_data() -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """Loads and formats the real Kuttanad dataset created by Teammate 1."""
    parcels_path = DATA_DIR / "sample_parcels.geojson"
    boundary_path = DATA_DIR / "canal_command_boundary.geojson"

    canal_network = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "id": "CANAL-AC-MAIN",
                    "name": "Alappuzha-Changanassery (AC) Main Canal",
                    "type": "Main Canal",
                    "flow_direction": "W",
                    "capacity_cumecs": 28.0
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [76.480, 9.520],
                        [76.450, 9.510],
                        [76.420, 9.495],
                        [76.390, 9.485]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "id": "CANAL-DIST-NORTH",
                    "name": "Kainakary North Distributary",
                    "type": "Distributary",
                    "flow_direction": "NW",
                    "capacity_cumecs": 10.0
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [76.450, 9.510],
                        [76.440, 9.535],
                        [76.425, 9.555]
                    ]
                }
            },
            {
                "type": "Feature",
                "properties": {
                    "id": "CANAL-DIST-SOUTH",
                    "name": "Nedumudi South Lateral",
                    "type": "Lateral",
                    "flow_direction": "SW",
                    "capacity_cumecs": 8.5
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [
                        [76.420, 9.495],
                        [76.410, 9.480],
                        [76.400, 9.468]
                    ]
                }
            }
        ]
    }

    if parcels_path.exists():
        with open(parcels_path, "r", encoding="utf-8") as f:
            raw_parcels = json.load(f)
        
        # Extract authentic pixel observations exclusively from Sentinel-2 MSI stack
        kuttanad_tif = DATA_DIR / "sentinel-2 data" / "kuttanad_sentinel_stack.tif"
        real_stats = {}
        if kuttanad_tif.exists():
            try:
                import rasterio
                from rasterio.mask import mask
                import numpy as np
                with rasterio.open(kuttanad_tif) as src:
                    for feat in raw_parcels.get("features", []):
                        pid = feat.get("properties", {}).get("parcel_id")
                        geom = [feat["geometry"]]
                        out_img, _ = mask(src, geom, crop=True)
                        valid = np.isfinite(out_img[0]) & (out_img[0] > -0.5) & np.isfinite(out_img[1])
                        if valid.any():
                            ndvi_m = float(np.nanmean(out_img[0, valid]))
                            ndwi_m = float(np.nanmean(out_img[1, valid]))
                            real_stats[pid] = {
                                "ndvi": round(ndvi_m, 4),
                                "ndwi": round(ndwi_m, 4),
                                "valid_pixels": int(valid.sum())
                            }
            except Exception as e:
                print(f"[GIS] Note reading kuttanad_sentinel_stack.tif: {e}")

        # Enrich raw features with authentic Sentinel-2 telemetry
        enriched_features = []
        for i, feat in enumerate(raw_parcels.get("features", [])):
            props = feat.get("properties", {})
            pid = props.get("parcel_id", f"PARCEL-K{i+1:03d}")
            crop = props.get("crop_type", "Paddy")
            block = props.get("canal_block", "BLOCK_NORTH_MAIN")
            
            reach = "head" if i < 2 else ("middle" if i < 4 else "tail")
            
            if pid not in real_stats:
                raise RuntimeError(f"Authentic Sentinel-2 data missing for parcel {pid}. Dummy fallbacks are prohibited.")
            
            sat = real_stats[pid]
            ndvi = sat["ndvi"]
            ndwi = sat["ndwi"]
            
            # Canopy water stress derived directly from authentic Sentinel-2 NDWI & NDVI
            # NDWI (Gao 1996) reflects leaf water content: lower NDWI indicates water stress
            # Normalized canopy moisture score: range [0.0 = severe stress, 1.0 = optimal hydration]
            hydration_score = float(np.clip((ndwi - 0.25) / 0.35, 0.05, 0.95))
            stress_score = round(1.0 - hydration_score, 2)
            
            if stress_score < 0.30:
                stress_level = "Normal"
            elif stress_score < 0.55:
                stress_level = "Mild"
            elif stress_score < 0.75:
                stress_level = "Moderate"
            else:
                stress_level = "Severe"

            def_m3 = round(stress_score * 320.0, 1)
            disc = round(stress_score * 3.0, 2)
            
            enriched_features.append({
                "type": "Feature",
                "id": pid,
                "properties": {
                    "id": pid,
                    "block_name": f"{block} ({reach.capitalize()})",
                    "reach": reach,
                    "crop_type": crop,
                    "crop_code": props.get("crop_code", 0),
                    "stage": "Tillering / Vegetative" if reach == "head" else "Flowering",
                    "stress_level": stress_level,
                    "stress_score": stress_score,
                    "ndvi": ndvi,
                    "ndwi": ndwi,
                    "deficit_m3_ha": def_m3,
                    "recommended_discharge": disc,
                    "area_ha": props.get("area_ha", 15.0),
                    "farmer": f"Kuttanad Polder #{i+1} (Authentic S2)",
                    "valid_s2_pixels": sat["valid_pixels"]
                },
                "geometry": feat.get("geometry")
            })
        
        parcels_collection = {
            "type": "FeatureCollection",
            "features": enriched_features
        }
    else:
        raise FileNotFoundError(f"Parcels GeoJSON missing at {parcels_path}. Dummy fallbacks prohibited.")

    return canal_network, parcels_collection


def get_command_system(command_area_id: str = "sirhind_punjab") -> Tuple[Dict[str, Any], Dict[str, Any]]:
    """
    Returns (canal_network_geojson, parcels_geojson) matching the selected region.
    """
    if "kuttanad" in command_area_id.lower() or "kerala" in command_area_id.lower():
        return load_kuttanad_data()
    
    # Default to Sirhind Canal Command, Punjab
    return SIRHIND_CANAL_NETWORK, SIRHIND_PARCELS_GEOJSON
