# Graph Report - Grove  (2026-09-26)

## Corpus Check
- 42 files · ~32,594 words
- Verdict: corpus is large enough that graph structure adds value.

## Summary
- 457 nodes · 659 edges · 25 communities (19 shown, 6 thin omitted)
- Extraction: 98% EXTRACTED · 2% INFERRED · 0% AMBIGUOUS · INFERRED: 15 edges (avg confidence: 0.5)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `243a8f26`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FastAPI Async REST Service
- App.tsx
- devDependencies
- gee_pipeline.py
- main.py
- 🔄 The Standard Parallel Git Lifecycle
- Grove (GeoPrithvi-Agri)
- compilerOptions
- compilerOptions
- test_data_loader.py
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

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 18 edges
2. `HydrologyEngine` - 17 edges
3. `compilerOptions` - 15 edges
4. `/graphify` - 13 edges
5. `What You Must Do When Invoked` - 13 edges
6. `compute_block_water_deficit()` - 11 edges
7. `get_command_system()` - 10 edges
8. `GEEPipeline` - 10 edges
9. `run_command_analysis()` - 10 edges
10. `load_feature_tensors()` - 9 edges

## Surprising Connections (you probably didn't know these)
- `test_effective_rainfall()` --calls--> `HydrologyEngine`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_hargreaves_et0()` --calls--> `HydrologyEngine`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_water_deficit_logic()` --calls--> `HydrologyEngine`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_interface_compute_block_water_deficit()` --calls--> `compute_block_water_deficit()`  [EXTRACTED]
  tests/test_hydrology.py → backend/hydrology.py
- `test_msf_net_dimensions()` --calls--> `MSFNetCropClassifier`  [EXTRACTED]
  tests/test_model.py → backend/model.py

## Import Cycles
- None detected.

## Communities (25 total, 6 thin omitted)

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
Cohesion: 0.16
Nodes (18): apply_refined_lee_filter(), build_composite_image(), compute_landsat_lst(), compute_sar_polarimetric_proxies(), compute_spectral_indices(), fetch_era5_meteorology(), mask_s2_clouds(), Any (+10 more)

### Community 4 - "main.py"
Cohesion: 0.07
Nodes (45): get_command_system(), load_kuttanad_data(), Any, Loads and formats the real Kuttanad dataset created by Teammate 1., Returns (canal_network_geojson, parcels_geojson) matching the selected region., GEEPipeline, Wrapper class providing high-level interface to Earth Engine routines., AnalysisInputPayload (+37 more)

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
Cohesion: 0.10
Nodes (20): get_available_satellite_chips(), GroveDataset, load_feature_tensors(), Any, Memory-Mapped Geospatial Data Loader & PyTorch Dataset Part of Grove…, Memory-Mapped PyTorch Dataset for streaming 10m Sentinel optical/SAR chip…, Returns all available authentic HLS / Sentinel satellite chips in the data…, Interface 1 Implementation: Memory-Mapped Geospatial Satellite Loader. Loads… (+12 more)

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
Nodes (34): Grove (GeoPrithvi-Agri) - High-Fidelity Agricultural GIS Datasets Provides…, extract_prithvi_embedding(), Executes a real forward pass on an authentic satellite chip using the IBM-NASA…, extract_feature_vector(), get_prithvi_model(), MSFNetCropClassifier, predict_crop_from_features(), Any (+26 more)

### Community 21 - "HydrologyEngine"
Cohesion: 0.13
Nodes (16): compute_block_water_deficit(), HydrologyEngine, Any, ndarray, Grove (GeoPrithvi-Agri) - Satellite Hydrology & Irrigation Deficit Engine…, USDA Soil Conservation Service (SCS) formula for 8-day effective precipitation…, Computes 8-day actual crop evapotranspiration, effective rainfall, and net…, Computes rigorous hydrological deficit and canal gate discharge release… (+8 more)

## Knowledge Gaps
- **146 isolated node(s):** `$schema`, `typescript`, `oxc`, `react/rules-of-hooks`, `warn` (+141 more)
  These have ≤1 connection - possible missing edges or undocumented components.
- **6 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `HydrologyEngine` connect `HydrologyEngine` to `main.py`?**
  _High betweenness centrality (0.017) - this node is a cross-community bridge._
- **Why does `compute_block_water_deficit()` connect `HydrologyEngine` to `main.py`?**
  _High betweenness centrality (0.010) - this node is a cross-community bridge._
- **Why does `devDependencies` connect `devDependencies` to `scripts`?**
  _High betweenness centrality (0.009) - this node is a cross-community bridge._
- **Are the 4 inferred relationships involving `HydrologyEngine` (e.g. with `AnalysisInputPayload` and `CanalAdvisoryItem`) actually correct?**
  _`HydrologyEngine` has 4 INFERRED edges - model-reasoned connections that need verification._
- **What connects `$schema`, `typescript`, `oxc` to the rest of the system?**
  _146 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FastAPI Async REST Service` be split into smaller, more focused modules?**
  _Cohesion score 0.06219512195121951 - nodes in this community are weakly interconnected._
- **Should `App.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.10106382978723404 - nodes in this community are weakly interconnected._