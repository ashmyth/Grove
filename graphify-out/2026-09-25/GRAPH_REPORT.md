# Graph Report - Grove  (2026-09-25)

## Corpus Check
- Corpus is ~10,791 words - fits in a single context window. You may not need a graph.

## Summary
- 42 nodes · 51 edges · 8 communities (7 shown, 1 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.5)
- Token cost: 1,250 input · 3,200 output

## Community Hubs (Navigation)
- Satellite Remote Sensing & Preprocessing
- Satellite Remote Sensing & Preprocessing
- Satellite Remote Sensing & Preprocessing
- Phenology & Moisture Stress Tracking
- Hydrological Deficit & Sluice Scheduling
- Hydrological Deficit & Sluice Scheduling
- Multimodal AI/ML & Foundation Models
- Multimodal AI/ML & Foundation Models

## God Nodes (most connected - your core abstractions)
1. `FastAPI Async REST Service` - 7 edges
2. `MSF-Net Asymmetric Late-Fusion Network` - 6 edges
3. `Google Earth Engine Preprocessing Pipeline` - 5 edges
4. `Region-Adaptive Phenology Alignment (RAM)` - 4 edges
5. `Composite Moisture Stress Index (CMSI)` - 4 edges
6. `8-Day Volumetric Water Deficit (m3/ha & mm)` - 4 edges
7. `React 18/19 + Vite Frontend Application` - 4 edges
8. `MapViewer Component (WebGL / Leaflet)` - 4 edges
9. `Memory-Mapped Raster Loader (rasterio)` - 3 edges
10. `Sentinel-2 MSI Optical Reflectance` - 3 edges

## Surprising Connections (you probably didn't know these)
- `Geospatial Data & ML Engineer` --references--> `MSF-Net Asymmetric Late-Fusion Network`  [EXTRACTED]
  prd.md → architecture.md
- `PMFBY Crop Insurance Auditor` --references--> `SAR Soil Moisture Index (SMI_SAR)`  [EXTRACTED]
  prd.md → architecture.md
- `Smallholder Farmer & FPO` --references--> `MapViewer Component (WebGL / Leaflet)`  [EXTRACTED]
  prd.md → architecture.md
- `Canal Command Engineer / Sluice Operator` --references--> `CanalAdvisory Component (Sluice Tables & Gauges)`  [EXTRACTED]
  prd.md → architecture.md
- `Agricultural Extension Officer` --references--> `PhenologyChart Component (Recharts Time-Series)`  [EXTRACTED]
  prd.md → architecture.md

## Communities (8 total, 1 thin omitted)

### Community 0 - "Satellite Remote Sensing & Preprocessing"
Cohesion: 0.25
Nodes (8): Composite Moisture Stress Index (CMSI), PMFBY Crop Insurance Auditor, Region-Adaptive Phenology Alignment (RAM), Savitzky-Golay Polynomial Smoother, SAR Soil Moisture Index (SMI_SAR), Split-Window LST Inversion, Thermal Anomaly Index (TAI_LST), Vegetation Condition Index (VCI)

### Community 1 - "Satellite Remote Sensing & Preprocessing"
Cohesion: 0.33
Nodes (7): Branch-Specific Auxiliary Loss Heads, Memory-Mapped Raster Loader (rasterio), Geospatial Data & ML Engineer, MSF-Net Asymmetric Late-Fusion Network, Prithvi-EO-1.0-100M ViT Backbone (Frozen), Scikit-Learn Random Forest Fallback, SAR Structural 2D CNN Patch Encoder

### Community 2 - "Satellite Remote Sensing & Preprocessing"
Cohesion: 0.29
Nodes (7): SCL Cloud Masking (NaN Filter), Google Earth Engine Preprocessing Pipeline, Landsat-8 TIRS Thermal Band 10, Polarimetric Decomposition (mv, ms), Refined Lee Speckle Filter (7x7), Sentinel-1 C-Band SAR GRD, Sentinel-2 MSI Optical Reflectance

### Community 3 - "Phenology & Moisture Stress Tracking"
Cohesion: 0.40
Nodes (6): GET /api/v1/crops/geojson, GET /api/v1/pixel/timeseries, GET /api/v1/stress/tiles, FastAPI Async REST Service, MapViewer Component (WebGL / Leaflet), Smallholder Farmer & FPO

### Community 4 - "Hydrological Deficit & Sluice Scheduling"
Cohesion: 0.40
Nodes (6): Effective Rainfall Model (Peff = 0.8*P), ECMWF ERA5-Land Meteorology Grids, FAO-56 Dynamic Crop Coefficients (Kc), Hargreaves-Samani ET0 Engine, Sluice Release Discharge Scheduler (Q = V/t), 8-Day Volumetric Water Deficit (m3/ha & mm)

### Community 5 - "Hydrological Deficit & Sluice Scheduling"
Cohesion: 0.50
Nodes (4): GET /api/v1/canals/advisories, CanalAdvisory Component (Sluice Tables & Gauges), Canal Command Engineer / Sluice Operator, ExportAdvisory Component (PDF / CSV)

### Community 6 - "Multimodal AI/ML & Foundation Models"
Cohesion: 0.67
Nodes (3): Agricultural Extension Officer, PhenologyChart Component (Recharts Time-Series), React 18/19 + Vite Frontend Application

## Knowledge Gaps
- **9 isolated node(s):** `Grove (GeoPrithvi-Agri)`, `SCL Cloud Masking (NaN Filter)`, `Scikit-Learn Random Forest Fallback`, `Branch-Specific Auxiliary Loss Heads`, `Savitzky-Golay Polynomial Smoother` (+4 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 9 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **1 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `FastAPI Async REST Service` connect `Phenology & Moisture Stress Tracking` to `Satellite Remote Sensing & Preprocessing`, `Satellite Remote Sensing & Preprocessing`, `Hydrological Deficit & Sluice Scheduling`, `Hydrological Deficit & Sluice Scheduling`?**
  _High betweenness centrality (0.546) - this node is a cross-community bridge._
- **Why does `Composite Moisture Stress Index (CMSI)` connect `Satellite Remote Sensing & Preprocessing` to `Phenology & Moisture Stress Tracking`?**
  _High betweenness centrality (0.311) - this node is a cross-community bridge._
- **Why does `MSF-Net Asymmetric Late-Fusion Network` connect `Satellite Remote Sensing & Preprocessing` to `Phenology & Moisture Stress Tracking`?**
  _High betweenness centrality (0.237) - this node is a cross-community bridge._
- **What connects `Grove (GeoPrithvi-Agri)`, `SCL Cloud Masking (NaN Filter)`, `Scikit-Learn Random Forest Fallback` to the rest of the system?**
  _9 weakly-connected nodes found - possible documentation gaps or missing edges._