# Graph Report - Grove  (2026-09-26)

## Corpus Check
- 47 files · ~35,382 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 492 nodes · 693 edges · 34 communities (28 shown, 6 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 18 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `f0380c44`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FastAPI Async REST Service
- App.tsx
- devDependencies
- gee_pipeline.py
- get
- 🔄 The Standard Parallel Git Lifecycle
- Grove (GeoPrithvi-Agri)
- compilerOptions
- compilerOptions
- test_data_loader.py
- dependencies
- plugins
- React + TypeScript + Vite
- tsconfig.json
- main.cjs
- /graphify
- preload.cjs
- predict_crop_from_features
- rules/graphify.md
- workflows/graphify.md
- HydrologyEngine
- ref_url
- Dataset Sources & Download Guide — Grove (GeoPrithvi-Agri)
- get_command_system
- main.py
- load_feature_tensors
- GeoPrithvi-Agri — Empirical Research & Training Protocols
- data_loader.py
- os
- model.py
- .compute_phenology_markers

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 18 edges
2. `HydrologyEngine` - 17 edges
3. `compilerOptions` - 15 edges
4. `/graphify` - 13 edges
5. `What You Must Do When Invoked` - 13 edges
6. `Dataset Sources & Download Guide — Grove (GeoPrithvi-Agri)` - 13 edges
7. `compute_block_water_deficit()` - 11 edges
8. `get_command_system()` - 10 edges
9. `GEEPipeline` - 10 edges
10. `run_command_analysis()` - 10 edges

## Surprising Connections (you probably didn't know these)
- `test_interface_1_contract()` --calls--> `load_feature_tensors()`  [EXTRACTED]
  tests/test_data_loader.py → backend/data_loader.py
- `test_effective_rainfall()` --calls--> `HydrologyEngine`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_hargreaves_et0()` --calls--> `HydrologyEngine`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_water_deficit_logic()` --calls--> `HydrologyEngine`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_interface_compute_block_water_deficit()` --calls--> `compute_block_water_deficit()`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py

## Import Cycles
- None detected.

## Communities (34 total, 6 thin omitted)

### Community 0 - "FastAPI Async REST Service"
Cohesion: 0.06
Nodes (41): Agricultural Extension Officer, GET /api/v1/canals/advisories, GET /api/v1/crops/geojson, GET /api/v1/pixel/timeseries, GET /api/v1/stress/tiles, Branch-Specific Auxiliary Loss Heads, CanalAdvisory Component (Sluice Tables & Gauges), Canal Command Engineer / Sluice Operator (+33 more)

### Community 1 - "App.tsx"
Cohesion: 0.10
Nodes (37): App(), AnalyticsDrawer(), AnalyticsDrawerProps, LandingConsole(), LandingConsoleProps, PRESET_AREAS, CommandControlBar(), CommandControlBarProps (+29 more)

### Community 2 - "devDependencies"
Cohesion: 0.08
Nodes (25): concurrently, cross-env, electron, devDependencies, concurrently, cross-env, electron, oxlint (+17 more)

### Community 3 - "gee_pipeline.py"
Cohesion: 0.17
Nodes (19): apply_refined_lee_filter(), build_composite_image(), compute_landsat_lst(), compute_sar_polarimetric_proxies(), compute_spectral_indices(), fetch_era5_meteorology(), mask_s2_clouds(), Any (+11 more)

### Community 4 - "get"
Cohesion: 0.15
Nodes (20): GEEPipeline, Wrapper class providing high-level interface to Earth Engine routines., AnalysisInputPayload, CanalAdvisoryItem, CommandOverview, enrich_parcels_with_ai(), get_canal_advisory(), get_command_overview() (+12 more)

### Community 6 - "🔄 The Standard Parallel Git Lifecycle"
Cohesion: 0.06
Nodes (34): 📚 Core Documentation, Grove (GeoPrithvi-Agri), 📄 License, 📌 Project Overview, 🛠️ Technology Stack, 1. Team Architectural Division & File Ownership, 2. Agent Execution Guides by Teammate, 3. Strict Interface Contracts Between Teammates (+26 more)

### Community 8 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 9 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 10 - "test_data_loader.py"
Cohesion: 0.09
Nodes (17): GroveDataset, Memory-Mapped PyTorch Dataset for streaming 10m Sentinel optical/SAR chip…, initialize_gee(), Authenticates and initializes Google Earth Engine session. Supports service…, Dataset, Grove (GeoPrithvi-Agri) Unified Single-Command Runner Launches the entire full-…, subprocess, sys (+9 more)

### Community 11 - "dependencies"
Cohesion: 0.06
Nodes (31): dependencies, gsap, leaflet, lucide-react, react, react-dom, react-leaflet, recharts (+23 more)

### Community 12 - "plugins"
Cohesion: 0.22
Nodes (8): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, typescript, warn

### Community 13 - "React + TypeScript + Vite"
Cohesion: 0.50
Nodes (3): Expanding the Oxlint configuration, React Compiler, React + TypeScript + Vite

### Community 15 - "main.cjs"
Cohesion: 0.33
Nodes (6): { app, BrowserWindow, ipcMain }, createWindow(), path, { spawn }, startBackend(), ref_path

### Community 16 - "/graphify"
Cohesion: 0.07
Nodes (28): For --cluster-only, For git commit hook, For /graphify add, For /graphify explain, For /graphify path, For /graphify query, For --update (incremental re-extraction), For --watch (+20 more)

### Community 18 - "predict_crop_from_features"
Cohesion: 0.09
Nodes (17): extract_feature_vector(), predict_crop_from_features(), Any, ndarray, RandomForestCropClassifier, Constructs normalized 7-dimensional feature vector exclusively from authentic…, Executes real inference on parcel Sentinel-2 signatures using the trained…, Deep Neural Network for Sentinel-2 Multi-Spectral Crop Classification. Operates… (+9 more)

### Community 21 - "HydrologyEngine"
Cohesion: 0.14
Nodes (15): compute_block_water_deficit(), HydrologyEngine, Any, ndarray, USDA Soil Conservation Service (SCS) formula for 8-day effective precipitation…, Computes 8-day actual crop evapotranspiration, effective rainfall, and net…, Computes rigorous hydrological deficit and canal gate discharge release…, Standard FAO-56 and PyET-compliant evapotranspiration and deficit engine. (+7 more)

### Community 25 - "Dataset Sources & Download Guide — Grove (GeoPrithvi-Agri)"
Cohesion: 0.14
Nodes (13): 10. 🌍 Landsat-8/9 OLI & MODIS, 1. 🛰️ Sentinel-2 MSI (Optical Multispectral), 2. 📡 Sentinel-1 C-Band SAR (GRD), 3. 🌤️ ERA5-Land Reanalysis (Meteorological), 4. 🗺️ Canal Command Area Shapefiles, 5. 🌡️ Landsat-8 TIRS Band 10 (Thermal Infrared), 6. 🏔️ SRTM Digital Elevation Model, 7. 🧠 IBM-NASA Prithvi Crop Classification Dataset (+5 more)

### Community 26 - "get_command_system"
Cohesion: 0.21
Nodes (10): get_command_system(), load_kuttanad_data(), Any, Grove (GeoPrithvi-Agri) - High-Fidelity Agricultural GIS Datasets Provides…, Loads and formats the real Kuttanad dataset created by Teammate 1., Returns (canal_network_geojson, parcels_geojson) matching the selected region., get_canal_network(), Grove (GeoPrithvi-Agri) - Authentic Sentinel-2 Crop Classification Training… (+2 more)

### Community 27 - "main.py"
Cohesion: 0.17
Nodes (12): get_diagnostics(), Grove (GeoPrithvi-Agri) FastAPI Backend Service Fully integrates Teammate 1…, Returns empirical evaluation metrics from the trained Random Forest and MSF-Net…, get_model_diagnostics(), Returns trained model performance metrics, confusion matrix, feature…, copy, fastapi, fastapi_middleware_cors (+4 more)

### Community 28 - "load_feature_tensors"
Cohesion: 0.20
Nodes (10): get_available_satellite_chips(), load_feature_tensors(), Any, Returns all available authentic HLS / Sentinel satellite chips and stacks in…, Interface 1 Implementation: Memory-Mapped Geospatial Satellite Loader. Loads…, extract_prithvi_embedding(), list_satellite_chips(), Returns catalog of authentic multi-temporal HLS 18-band satellite chips… (+2 more)

### Community 29 - "GeoPrithvi-Agri — Empirical Research & Training Protocols"
Cohesion: 0.18
Nodes (10): 1. Preprocessing Philosophy: 7-Day Linear Resampling, 2. Fusion Architecture: Asymmetric Late-Fusion (MSF-Net), 3. Loss Regularization: Multi-Task Auxiliary Supervision, 4. Ground-Truth Quality & Sample Thresholding, 5. Class Imbalance Strategy: Balanced Subset Undersampling, 6. Cross-Regional Generalization: Region-Aware Environmental Embeddings (RAM), 7. Transfer Learning & Sample Size Thresholds, 8. Sensor Complementarity: Tri-Modal Optical + SAR + Thermal Fusion (+2 more)

### Community 30 - "data_loader.py"
Cohesion: 0.38
Nodes (4): Memory-Mapped Geospatial Data Loader & PyTorch Dataset Part of Grove…, Grove (GeoPrithvi-Agri) - Satellite Hydrology & Irrigation Deficit Engine…, numpy, typing

### Community 31 - "os"
Cohesion: 0.29
Nodes (4): os, Download ERA5-Land meteorological data into data/era5_land/ Official Source:…, Download Sentinel-1 SAR & Sentinel-2 MSI data into data/sentinel1_sar/ and…, Download SRTM DEM & Landsat-8 TIRS Band 10 into data/srtm_dem/ and…

### Community 32 - "model.py"
Cohesion: 0.40
Nodes (5): get_prithvi_model(), Grove (GeoPrithvi-Agri) - Multi-Source Crop Classification AI Engine Trained…, Loads and caches the official IBM-NASA Prithvi-EO 100M foundation model…, Runs forward pass through the IBM-NASA Prithvi-EO 100M Foundation ViT. Input…, run_prithvi_embedding()

### Community 33 - ".compute_phenology_markers"
Cohesion: 0.40
Nodes (3): ndarray, Extracts SOS (Start of Season), Peak Vegetative, and LGP (Length of Growing…, Evaluates the Composite Moisture Stress Index (CMSI). stage-dependent weights:…

## Knowledge Gaps
- **168 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+163 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HydrologyEngine` connect `HydrologyEngine` to `main.py`, `get`, `data_loader.py`?**
  _High betweenness centrality (0.015) - this node is a cross-community bridge._
- **Why does `compute_block_water_deficit()` connect `HydrologyEngine` to `main.py`, `get`, `data_loader.py`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `devDependencies` connect `devDependencies` to `dependencies`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `HydrologyEngine` (e.g. with `AnalysisInputPayload` and `CanalAdvisoryItem`) actually correct?**
  _`HydrologyEngine` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `typescript`, `oxc` to the rest of the system?**
  _168 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FastAPI Async REST Service` be split into smaller, more focused modules?**
  _Cohesion score 0.06219512195121951 - nodes in this community are weakly interconnected._
- **Should `App.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.10106382978723404 - nodes in this community are weakly interconnected._