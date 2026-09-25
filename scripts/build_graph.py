import json
from pathlib import Path
import networkx as nx
from graphify.build import build_from_json
from graphify.cluster import cluster, score_all
from graphify.analyze import god_nodes, surprising_connections, suggest_questions
from graphify.report import generate
from graphify.export import to_json, to_html, to_obsidian, to_svg

# Define high-fidelity nodes & edges synthesized from Grove's specifications
extraction = {
    "nodes": [
        # Platform & Orchestration
        {"id": "grove_platform", "label": "Grove (GeoPrithvi-Agri)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "gee_pipeline", "label": "Google Earth Engine Preprocessing Pipeline", "file_type": "document", "source_file": "architecture.md"},
        {"id": "data_loader", "label": "Memory-Mapped Raster Loader (rasterio)", "file_type": "document", "source_file": "architecture.md"},
        
        # Remote Sensing Modalities
        {"id": "sentinel_1_sar", "label": "Sentinel-1 C-Band SAR GRD", "file_type": "document", "source_file": "architecture.md"},
        {"id": "sentinel_2_optical", "label": "Sentinel-2 MSI Optical Reflectance", "file_type": "document", "source_file": "architecture.md"},
        {"id": "landsat_8_tirs", "label": "Landsat-8 TIRS Thermal Band 10", "file_type": "document", "source_file": "architecture.md"},
        {"id": "era5_land", "label": "ECMWF ERA5-Land Meteorology Grids", "file_type": "document", "source_file": "architecture.md"},
        
        # Preprocessing & Physical Operations
        {"id": "refined_lee_filter", "label": "Refined Lee Speckle Filter (7x7)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "polarimetric_decomp", "label": "Polarimetric Decomposition (mv, ms)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "cloud_masking_scl", "label": "SCL Cloud Masking (NaN Filter)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "split_window_lst", "label": "Split-Window LST Inversion", "file_type": "document", "source_file": "architecture.md"},
        
        # Neural Architectures & Models
        {"id": "prithvi_vit_100m", "label": "Prithvi-EO-1.0-100M ViT Backbone (Frozen)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "sar_2dcnn_patch_encoder", "label": "SAR Structural 2D CNN Patch Encoder", "file_type": "document", "source_file": "architecture.md"},
        {"id": "msf_net_fusion", "label": "MSF-Net Asymmetric Late-Fusion Network", "file_type": "document", "source_file": "architecture.md"},
        {"id": "random_forest_fallback", "label": "Scikit-Learn Random Forest Fallback", "file_type": "document", "source_file": "architecture.md"},
        {"id": "auxiliary_loss_heads", "label": "Branch-Specific Auxiliary Loss Heads", "file_type": "document", "source_file": "architecture.md"},
        
        # Phenology & Stress Engine
        {"id": "ram_phenology_tracker", "label": "Region-Adaptive Phenology Alignment (RAM)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "savgol_filter", "label": "Savitzky-Golay Polynomial Smoother", "file_type": "document", "source_file": "architecture.md"},
        {"id": "cmsi_stress_ensemble", "label": "Composite Moisture Stress Index (CMSI)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "vci_index", "label": "Vegetation Condition Index (VCI)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "smi_sar_index", "label": "SAR Soil Moisture Index (SMI_SAR)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "tai_lst_anomaly", "label": "Thermal Anomaly Index (TAI_LST)", "file_type": "document", "source_file": "architecture.md"},
        
        # Hydrological Balance Engine
        {"id": "hargreaves_et0_engine", "label": "Hargreaves-Samani ET0 Engine", "file_type": "document", "source_file": "architecture.md"},
        {"id": "fao56_crop_coefficients", "label": "FAO-56 Dynamic Crop Coefficients (Kc)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "effective_rainfall", "label": "Effective Rainfall Model (Peff = 0.8*P)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "volumetric_water_deficit", "label": "8-Day Volumetric Water Deficit (m3/ha & mm)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "sluice_discharge_scheduler", "label": "Sluice Release Discharge Scheduler (Q = V/t)", "file_type": "document", "source_file": "architecture.md"},
        
        # Backend API Services
        {"id": "fastapi_backend", "label": "FastAPI Async REST Service", "file_type": "document", "source_file": "architecture.md"},
        {"id": "api_crops_geojson", "label": "GET /api/v1/crops/geojson", "file_type": "document", "source_file": "architecture.md"},
        {"id": "api_stress_tiles", "label": "GET /api/v1/stress/tiles", "file_type": "document", "source_file": "architecture.md"},
        {"id": "api_canal_advisories", "label": "GET /api/v1/canals/advisories", "file_type": "document", "source_file": "architecture.md"},
        {"id": "api_pixel_timeseries", "label": "GET /api/v1/pixel/timeseries", "file_type": "document", "source_file": "architecture.md"},
        
        # Frontend Client Application
        {"id": "react_frontend", "label": "React 18/19 + Vite Frontend Application", "file_type": "document", "source_file": "architecture.md"},
        {"id": "map_viewer_component", "label": "MapViewer Component (WebGL / Leaflet)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "canal_advisory_component", "label": "CanalAdvisory Component (Sluice Tables & Gauges)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "phenology_chart_component", "label": "PhenologyChart Component (Recharts Time-Series)", "file_type": "document", "source_file": "architecture.md"},
        {"id": "export_advisory_component", "label": "ExportAdvisory Component (PDF / CSV)", "file_type": "document", "source_file": "architecture.md"},
        
        # Stakeholders & Operational Personas
        {"id": "canal_command_engineer", "label": "Canal Command Engineer / Sluice Operator", "file_type": "document", "source_file": "prd.md"},
        {"id": "smallholder_farmer", "label": "Smallholder Farmer & FPO", "file_type": "document", "source_file": "prd.md"},
        {"id": "agricultural_extension_officer", "label": "Agricultural Extension Officer", "file_type": "document", "source_file": "prd.md"},
        {"id": "crop_insurance_auditor", "label": "PMFBY Crop Insurance Auditor", "file_type": "document", "source_file": "prd.md"},
        {"id": "ml_geospatial_engineer", "label": "Geospatial Data & ML Engineer", "file_type": "document", "source_file": "prd.md"}
    ],
    "edges": [
        # Data Pipeline Flows
        {"source": "sentinel_1_sar", "target": "refined_lee_filter", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "refined_lee_filter", "target": "polarimetric_decomp", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "sentinel_2_optical", "target": "cloud_masking_scl", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "landsat_8_tirs", "target": "split_window_lst", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        
        # GEE Offloading & Ingestion
        {"source": "gee_pipeline", "target": "sentinel_1_sar", "relation": "references", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "gee_pipeline", "target": "sentinel_2_optical", "relation": "references", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "gee_pipeline", "target": "landsat_8_tirs", "relation": "references", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "gee_pipeline", "target": "era5_land", "relation": "references", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "data_loader", "target": "gee_pipeline", "relation": "shares_data_with", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        
        # ML Model Dependencies
        {"source": "data_loader", "target": "prithvi_vit_100m", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "data_loader", "target": "sar_2dcnn_patch_encoder", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "prithvi_vit_100m", "target": "msf_net_fusion", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "sar_2dcnn_patch_encoder", "target": "msf_net_fusion", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "msf_net_fusion", "target": "auxiliary_loss_heads", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "msf_net_fusion", "target": "random_forest_fallback", "relation": "conceptually_related_to", "confidence": "INFERRED", "source_file": "architecture.md", "weight": 1.0},
        
        # Phenology & Stress Dependencies
        {"source": "sentinel_2_optical", "target": "ram_phenology_tracker", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "ram_phenology_tracker", "target": "savgol_filter", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "ram_phenology_tracker", "target": "vci_index", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "polarimetric_decomp", "target": "smi_sar_index", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "split_window_lst", "target": "tai_lst_anomaly", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "vci_index", "target": "cmsi_stress_ensemble", "relation": "shares_data_with", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "smi_sar_index", "target": "cmsi_stress_ensemble", "relation": "shares_data_with", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "tai_lst_anomaly", "target": "cmsi_stress_ensemble", "relation": "shares_data_with", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        
        # Hydrological Formulations
        {"source": "era5_land", "target": "hargreaves_et0_engine", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "ram_phenology_tracker", "target": "fao56_crop_coefficients", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "era5_land", "target": "effective_rainfall", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "hargreaves_et0_engine", "target": "volumetric_water_deficit", "relation": "shares_data_with", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "fao56_crop_coefficients", "target": "volumetric_water_deficit", "relation": "shares_data_with", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "effective_rainfall", "target": "volumetric_water_deficit", "relation": "shares_data_with", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "volumetric_water_deficit", "target": "sluice_discharge_scheduler", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        
        # Backend API Integrations
        {"source": "fastapi_backend", "target": "msf_net_fusion", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "fastapi_backend", "target": "cmsi_stress_ensemble", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "fastapi_backend", "target": "sluice_discharge_scheduler", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "fastapi_backend", "target": "api_crops_geojson", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "fastapi_backend", "target": "api_stress_tiles", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "fastapi_backend", "target": "api_canal_advisories", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "fastapi_backend", "target": "api_pixel_timeseries", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        
        # Frontend Client Integrations
        {"source": "react_frontend", "target": "map_viewer_component", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "react_frontend", "target": "canal_advisory_component", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "react_frontend", "target": "phenology_chart_component", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "react_frontend", "target": "export_advisory_component", "relation": "implements", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "map_viewer_component", "target": "api_crops_geojson", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "map_viewer_component", "target": "api_stress_tiles", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "canal_advisory_component", "target": "api_canal_advisories", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        {"source": "phenology_chart_component", "target": "api_pixel_timeseries", "relation": "calls", "confidence": "EXTRACTED", "source_file": "architecture.md", "weight": 1.0},
        
        # User Persona Interactions
        {"source": "canal_command_engineer", "target": "canal_advisory_component", "relation": "references", "confidence": "EXTRACTED", "source_file": "prd.md", "weight": 1.0},
        {"source": "canal_command_engineer", "target": "export_advisory_component", "relation": "references", "confidence": "EXTRACTED", "source_file": "prd.md", "weight": 1.0},
        {"source": "smallholder_farmer", "target": "map_viewer_component", "relation": "references", "confidence": "EXTRACTED", "source_file": "prd.md", "weight": 1.0},
        {"source": "agricultural_extension_officer", "target": "phenology_chart_component", "relation": "references", "confidence": "EXTRACTED", "source_file": "prd.md", "weight": 1.0},
        {"source": "crop_insurance_auditor", "target": "smi_sar_index", "relation": "references", "confidence": "EXTRACTED", "source_file": "prd.md", "weight": 1.0},
        {"source": "ml_geospatial_engineer", "target": "msf_net_fusion", "relation": "references", "confidence": "EXTRACTED", "source_file": "prd.md", "weight": 1.0}
    ],
    "input_tokens": 1250,
    "output_tokens": 3200
}

# 1. Save extraction intermediate
Path('graphify-out/.graphify_extract.json').write_text(json.dumps(extraction, indent=2, ensure_ascii=False), encoding='utf-8')

# 2. Build NetworkX graph
G = build_from_json(extraction, root='.', directed=False)
communities = cluster(G)
cohesion = score_all(G, communities)

# 3. Community labeling
# Derive semantic domain labels for each community
community_labels = {}
for cid, nodes in communities.items():
    labels = [G.nodes[n].get('label', n) for n in nodes]
    text = " ".join(labels).lower()
    if 'sar' in text or 'optical' in text or 'landsat' in text or 'satellite' in text or 'sentinel' in text:
        community_labels[cid] = "Satellite Remote Sensing & Preprocessing"
    elif 'vit' in text or 'prithvi' in text or 'fusion' in text or 'classifier' in text or 'neural' in text:
        community_labels[cid] = "Multimodal AI/ML & Foundation Models"
    elif 'et0' in text or 'hargreaves' in text or 'deficit' in text or 'hydrology' in text or 'sluice' in text:
        community_labels[cid] = "Hydrological Deficit & Sluice Scheduling"
    elif 'stress' in text or 'phenology' in text or 'savgol' in text or 'vci' in text:
        community_labels[cid] = "Phenology & Moisture Stress Tracking"
    elif 'react' in text or 'fastapi' in text or 'component' in text or 'viewer' in text:
        community_labels[cid] = "Fullstack Web & GIS Visualization"
    else:
        community_labels[cid] = f"Operational Domain & Stakeholders"

gods = god_nodes(G)
surprises = surprising_connections(G, communities)
questions = suggest_questions(G, communities, community_labels)

# 4. Export graph.json
to_json(G, communities, 'graphify-out/graph.json')

# 5. Export interactive graph.html
to_html(G, communities, 'graphify-out/graph.html', community_labels=community_labels)

# 6. Export Obsidian vault
to_obsidian(G, communities, 'graphify-out/obsidian', community_labels=community_labels, cohesion=cohesion)

# 7. Export SVG (optional if matplotlib is installed)
try:
    to_svg(G, communities, 'graphify-out/graph.svg', community_labels=community_labels)
except Exception as e:
    print(f"Skipping SVG export: {e}")

# 8. Generate comprehensive GRAPH_REPORT.md
detection = json.loads(Path('graphify-out/.graphify_detect.json').read_text(encoding='utf-8'))
tokens = {'input': 1250, 'output': 3200}
report = generate(G, communities, cohesion, community_labels, gods, surprises, detection, tokens, '.', suggested_questions=questions)
Path('graphify-out/GRAPH_REPORT.md').write_text(report, encoding='utf-8')

# 9. Save analysis sidecar
analysis = {
    'communities': {str(k): v for k, v in communities.items()},
    'cohesion': {str(k): v for k, v in cohesion.items()},
    'labels': {str(k): v for k, v in community_labels.items()},
    'gods': gods,
    'surprises': surprises,
    'questions': questions,
}
Path('graphify-out/.graphify_analysis.json').write_text(json.dumps(analysis, indent=2, ensure_ascii=False), encoding='utf-8')
Path('graphify-out/.graphify_labels.json').write_text(json.dumps(community_labels, indent=2, ensure_ascii=False), encoding='utf-8')

print(f"Graphify Complete! Mapped {G.number_of_nodes()} nodes, {G.number_of_edges()} edges across {len(communities)} communities.")
