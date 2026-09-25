# Graph Report - Grove  (2026-09-25)

## Corpus Check
- 39 files · ~29,350 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .geojson 2, .css 2)

## Summary
- 425 nodes · 575 edges · 24 communities (17 shown, 7 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 4 edges (avg confidence: 0.6)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `c86cbd4f`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- FastAPI Async REST Service
- App.tsx
- devDependencies
- test_data_loader.py
- main.py
- 🔄 The Standard Parallel Git Lifecycle
- Grove (GeoPrithvi-Agri)
- compilerOptions
- compilerOptions
- gee_pipeline.py
- package.json
- plugins
- React + TypeScript + Vite
- tsconfig.json
- main.ts
- /graphify
- test_model.py
- rules/graphify.md
- workflows/graphify.md
- HydrologyEngine
- start.py
- Any

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 18 edges
2. `compilerOptions` - 15 edges
3. `/graphify` - 13 edges
4. `What You Must Do When Invoked` - 13 edges
5. `get_command_system()` - 10 edges
6. `run_command_analysis()` - 8 edges
7. `GroveDataset` - 8 edges
8. `HydrologyEngine` - 8 edges
9. `react` - 8 edges
10. `scripts` - 8 edges

## Surprising Connections (you probably didn't know these)
- `test_gee_pipeline_graceful()` --calls--> `initialize_gee()`  [EXTRACTED]
  tests/test_data_loader.py → backend/gee_pipeline.py
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

## Communities (24 total, 7 thin omitted)

### Community 0 - "FastAPI Async REST Service"
Cohesion: 0.06
Nodes (41): Agricultural Extension Officer, GET /api/v1/canals/advisories, GET /api/v1/crops/geojson, GET /api/v1/pixel/timeseries, GET /api/v1/stress/tiles, Branch-Specific Auxiliary Loss Heads, CanalAdvisory Component (Sluice Tables & Gauges), Canal Command Engineer / Sluice Operator (+33 more)

### Community 1 - "App.tsx"
Cohesion: 0.12
Nodes (33): App(), AnalyticsDrawer(), AnalyticsDrawerProps, CommandControlBar(), CommandControlBarProps, Header(), HeaderProps, MapViewer() (+25 more)

### Community 2 - "devDependencies"
Cohesion: 0.08
Nodes (25): concurrently, cross-env, electron, devDependencies, concurrently, cross-env, electron, oxlint (+17 more)

### Community 3 - "test_data_loader.py"
Cohesion: 0.10
Nodes (21): _generate_fallback_dict(), GroveDataset, load_feature_tensors(), Any, Memory-Mapped Geospatial Data Loader & PyTorch Dataset Part of Grove…, Generates synthetic memory-mapped feature tensors matching Interface 1…, Memory-Mapped PyTorch Dataset for streaming 10m Sentinel optical/SAR chip…, Interface 1 Implementation (Teammate 1 -> Teammate 2) Args: sample_id: Unique… (+13 more)

### Community 4 - "main.py"
Cohesion: 0.07
Nodes (38): Any, get_command_system(), load_kuttanad_data(), Grove (GeoPrithvi-Agri) - High-Fidelity Agricultural GIS Datasets Provides…, Loads and formats the real Kuttanad dataset created by Teammate 1., Returns (canal_network_geojson, parcels_geojson) matching the selected region., AnalysisInputPayload, CanalAdvisoryItem (+30 more)

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
Cohesion: 0.11
Nodes (23): apply_refined_lee_filter(), build_composite_image(), compute_landsat_lst(), compute_sar_polarimetric_proxies(), compute_spectral_indices(), fetch_era5_meteorology(), GEEPipeline, initialize_gee() (+15 more)

### Community 11 - "package.json"
Cohesion: 0.07
Nodes (28): dependencies, leaflet, lucide-react, react, react-dom, react-leaflet, recharts, @types/leaflet (+20 more)

### Community 12 - "plugins"
Cohesion: 0.22
Nodes (8): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema, oxc, typescript, warn

### Community 13 - "React + TypeScript + Vite"
Cohesion: 0.50
Nodes (3): Expanding the Oxlint configuration, React Compiler, React + TypeScript + Vite

### Community 15 - "main.ts"
Cohesion: 0.20
Nodes (6): { app, BrowserWindow }, __dirname, __filename, path, ref_path, ref_url

### Community 16 - "/graphify"
Cohesion: 0.07
Nodes (28): For --cluster-only, For git commit hook, For /graphify add, For /graphify explain, For /graphify path, For /graphify query, For --update (incremental re-extraction), For --watch (+20 more)

### Community 18 - "test_model.py"
Cohesion: 0.14
Nodes (14): MSFNetCropClassifier, PrithviFeatureExtractor, ndarray, RandomForestCropClassifier, optical_seq: (B, T, C=6, H=224, W=224) sar_patches: (B, C=2, H=11, W=11), Interface Contract 2: ML / Hydrology -> FastAPI Backend Returns 2D integer…, run_crop_inference(), SARPatchEncoder (+6 more)

### Community 21 - "HydrologyEngine"
Cohesion: 0.24
Nodes (10): compute_block_water_deficit(), HydrologyEngine, ndarray, Computes effective rainfall, crop evapotranspiration, and 8-day water deficit., Interface Contract 2: ML / Hydrology -> FastAPI Backend, Computes daily Reference Evapotranspiration (ETo) in mm/day using Hargreaves-…, test_effective_rainfall(), test_hargreaves_et0() (+2 more)

### Community 22 - "start.py"
Cohesion: 0.29
Nodes (5): main(), Grove (GeoPrithvi-Agri) Unified Single-Command Runner Launches the entire full-…, subprocess, time, webbrowser

## Knowledge Gaps
- **143 isolated node(s):** `StressLevel`, `ParcelProperties`, `CanalLineFeature`, `$schema`, `typescript` (+138 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 210 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **7 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `devDependencies` connect `devDependencies` to `package.json`?**
  _High betweenness centrality (0.011) - this node is a cross-community bridge._
- **What connects `StressLevel`, `ParcelProperties`, `CanalLineFeature` to the rest of the system?**
  _143 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `FastAPI Async REST Service` be split into smaller, more focused modules?**
  _Cohesion score 0.06219512195121951 - nodes in this community are weakly interconnected._
- **Should `App.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.11614401858304298 - nodes in this community are weakly interconnected._
- **Should `devDependencies` be split into smaller, more focused modules?**
  _Cohesion score 0.08 - nodes in this community are weakly interconnected._
- **Should `test_data_loader.py` be split into smaller, more focused modules?**
  _Cohesion score 0.10256410256410256 - nodes in this community are weakly interconnected._
- **Should `main.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07373737373737374 - nodes in this community are weakly interconnected._