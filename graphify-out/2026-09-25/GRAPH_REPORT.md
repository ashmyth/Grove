# Graph Report - Grove  (2026-09-25)

## Corpus Check
- 37 files · ~26,646 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 8 file(s) not represented in the graph (top: (none) 4, .geojson 2, .css 2)

## Summary
- 274 nodes · 355 edges · 18 communities (15 shown, 3 thin omitted)
- Extraction: 99% EXTRACTED · 1% INFERRED · 0% AMBIGUOUS · INFERRED: 3 edges (avg confidence: 0.75)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `fa9b1b77`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Google Earth Engine Preprocessing Pipeline
- App.tsx
- devDependencies
- FastAPI Async REST Service
- main.py
- package.json
- 🔄 The Standard Parallel Git Lifecycle
- Grove (GeoPrithvi-Agri)
- compilerOptions
- compilerOptions
- gee_pipeline.py
- dependencies
- .oxlintrc.json
- React + TypeScript + Vite
- tsconfig.json
- main.ts
- scripts

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 18 edges
2. `compilerOptions` - 15 edges
3. `scripts` - 8 edges
4. `react` - 7 edges
5. `build_composite_image()` - 7 edges
6. `FastAPI Async REST Service` - 7 edges
7. `App()` - 6 edges
8. `🔄 The Standard Parallel Git Lifecycle` - 6 edges
9. `MSF-Net Asymmetric Late-Fusion Network` - 6 edges
10. `CanalAdvisoryItem` - 5 edges

## Surprising Connections (you probably didn't know these)
- `Geospatial Data & ML Engineer` --references--> `MSF-Net Asymmetric Late-Fusion Network`  [EXTRACTED]
  prd.md → architecture.md
- `PMFBY Crop Insurance Auditor` --references--> `SAR Soil Moisture Index (SMI_SAR)`  [EXTRACTED]
  prd.md → architecture.md
- `Agricultural Extension Officer` --references--> `PhenologyChart Component (Recharts Time-Series)`  [EXTRACTED]
  prd.md → architecture.md
- `Canal Command Engineer / Sluice Operator` --references--> `CanalAdvisory Component (Sluice Tables & Gauges)`  [EXTRACTED]
  prd.md → architecture.md
- `Canal Command Engineer / Sluice Operator` --references--> `ExportAdvisory Component (PDF / CSV)`  [EXTRACTED]
  prd.md → architecture.md

## Import Cycles
- None detected.

## Communities (18 total, 3 thin omitted)

### Community 0 - "Google Earth Engine Preprocessing Pipeline"
Cohesion: 0.11
Nodes (21): SCL Cloud Masking (NaN Filter), Composite Moisture Stress Index (CMSI), PMFBY Crop Insurance Auditor, Effective Rainfall Model (Peff = 0.8*P), ECMWF ERA5-Land Meteorology Grids, FAO-56 Dynamic Crop Coefficients (Kc), Google Earth Engine Preprocessing Pipeline, Hargreaves-Samani ET0 Engine (+13 more)

### Community 1 - "App.tsx"
Cohesion: 0.13
Nodes (30): App(), AnalyticsDrawer(), AnalyticsDrawerProps, Header(), HeaderProps, MapViewer(), MapViewerProps, CanalTelemetry() (+22 more)

### Community 2 - "devDependencies"
Cohesion: 0.15
Nodes (13): devDependencies, concurrently, cross-env, electron, oxlint, tailwindcss, @tailwindcss/vite, @types/node (+5 more)

### Community 3 - "FastAPI Async REST Service"
Cohesion: 0.13
Nodes (20): Agricultural Extension Officer, GET /api/v1/canals/advisories, GET /api/v1/crops/geojson, GET /api/v1/pixel/timeseries, GET /api/v1/stress/tiles, Branch-Specific Auxiliary Loss Heads, CanalAdvisory Component (Sluice Tables & Gauges), Canal Command Engineer / Sluice Operator (+12 more)

### Community 4 - "main.py"
Cohesion: 0.13
Nodes (22): CanalAdvisoryItem, CommandOverview, get_canal_advisory(), get_canal_network(), get_command_overview(), get_parcels_geojson(), get_pixel_timeseries(), health_check() (+14 more)

### Community 5 - "package.json"
Cohesion: 0.11
Nodes (18): main, name, private, type, version, concurrently, cross-env, oxlint (+10 more)

### Community 6 - "🔄 The Standard Parallel Git Lifecycle"
Cohesion: 0.07
Nodes (29): 1. Team Architectural Division & File Ownership, 2. Agent Execution Guides by Teammate, 3. Strict Interface Contracts Between Teammates, 4. Git Parallel Workflow & Collaboration Rules, 🎯 Agent Mission:, 🎯 Agent Mission:, 🎯 Agent Mission:, 📂 Files You Own: (+21 more)

### Community 8 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 9 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 10 - "gee_pipeline.py"
Cohesion: 0.10
Nodes (25): Any, apply_refined_lee_filter(), build_composite_image(), compute_landsat_lst(), compute_sar_polarimetric_proxies(), compute_spectral_indices(), fetch_era5_meteorology(), GEEPipeline (+17 more)

### Community 11 - "dependencies"
Cohesion: 0.25
Nodes (8): dependencies, leaflet, lucide-react, react, react-dom, react-leaflet, recharts, @types/leaflet

### Community 12 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 13 - "React + TypeScript + Vite"
Cohesion: 0.50
Nodes (3): Expanding the Oxlint configuration, React Compiler, React + TypeScript + Vite

### Community 15 - "main.ts"
Cohesion: 0.20
Nodes (7): { app, BrowserWindow }, __dirname, __filename, path, electron, ref_path, ref_url

### Community 16 - "scripts"
Cohesion: 0.25
Nodes (8): scripts, build, dev, electron:build, electron:dev, electron:start, lint, preview

## Knowledge Gaps
- **120 isolated node(s):** `{ app, BrowserWindow }`, `path`, `__filename`, `__dirname`, `name` (+115 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 154 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **3 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `App.tsx` to `package.json`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `devDependencies` connect `devDependencies` to `package.json`?**
  _High betweenness centrality (0.029) - this node is a cross-community bridge._
- **Why does `electron` connect `main.ts` to `package.json`?**
  _High betweenness centrality (0.024) - this node is a cross-community bridge._
- **What connects `{ app, BrowserWindow }`, `path`, `__filename` to the rest of the system?**
  _120 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Google Earth Engine Preprocessing Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.11428571428571428 - nodes in this community are weakly interconnected._
- **Should `App.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.1251778093883357 - nodes in this community are weakly interconnected._
- **Should `FastAPI Async REST Service` be split into smaller, more focused modules?**
  _Cohesion score 0.12631578947368421 - nodes in this community are weakly interconnected._