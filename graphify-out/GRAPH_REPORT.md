# Graph Report - Grove  (2026-09-26)

## Corpus Check
- 47 files · ~34,863 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 481 nodes · 685 edges · 25 communities (19 shown, 6 thin omitted)
- Extraction: 97% EXTRACTED · 3% INFERRED · 0% AMBIGUOUS · INFERRED: 18 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `4452740e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FastAPI Async REST Service
- App.tsx
- devDependencies
- main.py
- 🔄 The Standard Parallel Git Lifecycle
- Grove (GeoPrithvi-Agri)
- compilerOptions
- compilerOptions
- gee_pipeline.py
- scripts
- plugins
- React + TypeScript + Vite
- tsconfig.json
- main.cjs
- /graphify
- preload.cjs
- model.py
- rules/graphify.md
- workflows/graphify.md
- HydrologyEngine
- ref_url
- Dataset Sources & Download Guide — Grove (GeoPrithvi-Agri)

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
- `test_effective_rainfall()` --calls--> `HydrologyEngine`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_hargreaves_et0()` --calls--> `HydrologyEngine`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_water_deficit_logic()` --calls--> `HydrologyEngine`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_interface_compute_block_water_deficit()` --calls--> `compute_block_water_deficit()`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_random_forest_fallback()` --calls--> `RandomForestCropClassifier`  [EXTRACTED]
  tests/test_model.py → backend/model.py

## Import Cycles
- None detected.

## Communities (25 total, 6 thin omitted)

### Community 0 - "FastAPI Async REST Service"
Cohesion: 0.06
Nodes (41): Agricultural Extension Officer, GET /api/v1/canals/advisories, GET /api/v1/crops/geojson, GET /api/v1/pixel/timeseries, GET /api/v1/stress/tiles, Branch-Specific Auxiliary Loss Heads, CanalAdvisory Component (Sluice Tables & Gauges), Canal Command Engineer / Sluice Operator (+33 more)

### Community 1 - "App.tsx"
Cohesion: 0.10
Nodes (38): App(), AnalyticsDrawer(), AnalyticsDrawerProps, LandingConsole(), LandingConsoleProps, PRESET_AREAS, CommandControlBar(), CommandControlBarProps (+30 more)

### Community 2 - "devDependencies"
Cohesion: 0.08
Nodes (25): concurrently, cross-env, electron, devDependencies, concurrently, cross-env, electron, oxlint (+17 more)

### Community 4 - "main.py"
Cohesion: 0.07
Nodes (45): get_command_system(), load_kuttanad_data(), Any, Loads and formats the real Kuttanad dataset created by Teammate 1., Returns (canal_network_geojson, parcels_geojson) matching the selected region., get_available_satellite_chips(), Returns all available authentic HLS / Sentinel satellite chips and stacks in…, GEEPipeline (+37 more)

### Community 6 - "🔄 The Standard Parallel Git Lifecycle"
Cohesion: 0.06
Nodes (34): 📚 Core Documentation, Grove (GeoPrithvi-Agri), 📄 License, 📌 Project Overview, 🛠️ Technology Stack, 1. Team Architectural Division & File Ownership, 2. Agent Execution Guides by Teammate, 3. Strict Interface Contracts Between Teammates (+26 more)

### Community 8 - "compilerOptions"
Cohesion: 0.08
Nodes (23): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+15 more)

### Community 9 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+11 more)

### Community 10 - "gee_pipeline.py"
Cohesion: 0.06
Nodes (40): GroveDataset, load_feature_tensors(), Any, Memory-Mapped PyTorch Dataset for streaming 10m Sentinel optical/SAR chip…, Interface 1 Implementation: Memory-Mapped Geospatial Satellite Loader. Loads…, apply_refined_lee_filter(), build_composite_image(), compute_landsat_lst() (+32 more)

### Community 11 - "scripts"
Cohesion: 0.07
Nodes (29): dependencies, leaflet, lucide-react, react, react-dom, react-leaflet, recharts, @types/leaflet (+21 more)

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

### Community 18 - "model.py"
Cohesion: 0.06
Nodes (34): Grove (GeoPrithvi-Agri) - High-Fidelity Agricultural GIS Datasets Provides…, Memory-Mapped Geospatial Data Loader & PyTorch Dataset Part of Grove…, extract_feature_vector(), get_prithvi_model(), predict_crop_from_features(), Any, ndarray, RandomForestCropClassifier (+26 more)

### Community 21 - "HydrologyEngine"
Cohesion: 0.12
Nodes (17): compute_block_water_deficit(), HydrologyEngine, Any, ndarray, Grove (GeoPrithvi-Agri) - Satellite Hydrology & Irrigation Deficit Engine…, USDA Soil Conservation Service (SCS) formula for 8-day effective precipitation…, Computes 8-day actual crop evapotranspiration, effective rainfall, and net…, Computes rigorous hydrological deficit and canal gate discharge release… (+9 more)

### Community 25 - "Dataset Sources & Download Guide — Grove (GeoPrithvi-Agri)"
Cohesion: 0.14
Nodes (13): 10. 🌍 Landsat-8/9 OLI & MODIS, 1. 🛰️ Sentinel-2 MSI (Optical Multispectral), 2. 📡 Sentinel-1 C-Band SAR (GRD), 3. 🌤️ ERA5-Land Reanalysis (Meteorological), 4. 🗺️ Canal Command Area Shapefiles, 5. 🌡️ Landsat-8 TIRS Band 10 (Thermal Infrared), 6. 🏔️ SRTM Digital Elevation Model, 7. 🧠 IBM-NASA Prithvi Crop Classification Dataset (+5 more)

## Knowledge Gaps
- **158 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+153 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HydrologyEngine` connect `HydrologyEngine` to `main.py`?**
  _High betweenness centrality (0.016) - this node is a cross-community bridge._
- **Why does `compute_block_water_deficit()` connect `HydrologyEngine` to `main.py`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Why does `PhenologyStressEngine` connect `main.py` to `model.py`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `HydrologyEngine` (e.g. with `AnalysisInputPayload` and `CanalAdvisoryItem`) actually correct?**
  _`HydrologyEngine` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `typescript`, `oxc` to the rest of the system?**
  _158 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FastAPI Async REST Service` be split into smaller, more focused modules?**
  _Cohesion score 0.06219512195121951 - nodes in this community are weakly interconnected._
- **Should `App.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.0963265306122449 - nodes in this community are weakly interconnected._