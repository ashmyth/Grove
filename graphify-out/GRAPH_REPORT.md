# Graph Report - Grove  (2026-09-25)

## Corpus Check
- 24 files · ~21,198 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 6 file(s) not represented in the graph (top: (none) 4, .css 2)

## Summary
- 223 nodes · 291 edges · 15 communities (13 shown, 2 thin omitted)
- Extraction: 100% EXTRACTED · 0% INFERRED · 0% AMBIGUOUS · INFERRED: 1 edges (avg confidence: 0.55)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `ffa1f8ef`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- Google Earth Engine Preprocessing Pipeline
- App.tsx
- 🔄 The Standard Parallel Git Lifecycle
- FastAPI Async REST Service
- main.py
- package.json
- 🛰️ Teammate 1: Remote Sensing & Data Pipeline Engineer
- Grove (GeoPrithvi-Agri)
- compilerOptions
- compilerOptions
- devDependencies
- dependencies
- .oxlintrc.json
- React + TypeScript + Vite
- tsconfig.json

## God Nodes (most connected - your core abstractions)
1. `compilerOptions` - 18 edges
2. `compilerOptions` - 15 edges
3. `react` - 7 edges
4. `FastAPI Async REST Service` - 7 edges
5. `App()` - 6 edges
6. `🔄 The Standard Parallel Git Lifecycle` - 6 edges
7. `MSF-Net Asymmetric Late-Fusion Network` - 6 edges
8. `scripts` - 5 edges
9. `CanalAdvisoryItem` - 5 edges
10. `CommandOverview` - 5 edges

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

## Communities (15 total, 2 thin omitted)

### Community 0 - "Google Earth Engine Preprocessing Pipeline"
Cohesion: 0.11
Nodes (21): SCL Cloud Masking (NaN Filter), Composite Moisture Stress Index (CMSI), PMFBY Crop Insurance Auditor, Effective Rainfall Model (Peff = 0.8*P), ECMWF ERA5-Land Meteorology Grids, FAO-56 Dynamic Crop Coefficients (Kc), Google Earth Engine Preprocessing Pipeline, Hargreaves-Samani ET0 Engine (+13 more)

### Community 1 - "App.tsx"
Cohesion: 0.13
Nodes (30): App(), AnalyticsDrawer(), AnalyticsDrawerProps, Header(), HeaderProps, MapViewer(), MapViewerProps, CanalTelemetry() (+22 more)

### Community 2 - "🔄 The Standard Parallel Git Lifecycle"
Cohesion: 0.14
Nodes (13): 1. Team Architectural Division & File Ownership, 3. Strict Interface Contracts Between Teammates, 4. Git Parallel Workflow & Collaboration Rules, Interface 1: Data Pipeline ➡️ ML / Hydrology (Teammate 1 ➡️ Teammate 2), Interface 2: ML / Hydrology ➡️ FastAPI Backend (Teammate 2 ➡️ Teammate 3), Interface 3: FastAPI Backend ➡️ React Frontend (Teammate 3 Backend ➡️ Frontend), Step 1: Starting Your Task, Step 2: Committing Your Work (+5 more)

### Community 3 - "FastAPI Async REST Service"
Cohesion: 0.13
Nodes (20): Agricultural Extension Officer, GET /api/v1/canals/advisories, GET /api/v1/crops/geojson, GET /api/v1/pixel/timeseries, GET /api/v1/stress/tiles, Branch-Specific Auxiliary Loss Heads, CanalAdvisory Component (Sluice Tables & Gauges), Canal Command Engineer / Sluice Operator (+12 more)

### Community 4 - "main.py"
Cohesion: 0.13
Nodes (22): CanalAdvisoryItem, CommandOverview, get_canal_advisory(), get_canal_network(), get_command_overview(), get_parcels_geojson(), get_pixel_timeseries(), health_check() (+14 more)

### Community 5 - "package.json"
Cohesion: 0.10
Nodes (20): name, private, scripts, build, dev, lint, preview, type (+12 more)

### Community 6 - "🛰️ Teammate 1: Remote Sensing & Data Pipeline Engineer"
Cohesion: 0.12
Nodes (16): 2. Agent Execution Guides by Teammate, 🎯 Agent Mission:, 🎯 Agent Mission:, 🎯 Agent Mission:, 📂 Files You Own:, 📂 Files You Own:, 📂 Files You Own:, 🚫 Scope Fence (DO NOT TOUCH): (+8 more)

### Community 8 - "compilerOptions"
Cohesion: 0.10
Nodes (19): compilerOptions, allowArbitraryExtensions, allowImportingTsExtensions, erasableSyntaxOnly, jsx, lib, module, moduleDetection (+11 more)

### Community 9 - "compilerOptions"
Cohesion: 0.12
Nodes (16): compilerOptions, allowImportingTsExtensions, erasableSyntaxOnly, lib, module, moduleDetection, noEmit, noFallthroughCasesInSwitch (+8 more)

### Community 10 - "devDependencies"
Cohesion: 0.20
Nodes (10): devDependencies, oxlint, tailwindcss, @tailwindcss/vite, @types/node, @types/react, @types/react-dom, typescript (+2 more)

### Community 11 - "dependencies"
Cohesion: 0.25
Nodes (8): dependencies, leaflet, lucide-react, react, react-dom, react-leaflet, recharts, @types/leaflet

### Community 12 - ".oxlintrc.json"
Cohesion: 0.33
Nodes (5): plugins, rules, react/only-export-components, react/rules-of-hooks, $schema

### Community 13 - "React + TypeScript + Vite"
Cohesion: 0.50
Nodes (3): Expanding the Oxlint configuration, React Compiler, React + TypeScript + Vite

## Knowledge Gaps
- **107 isolated node(s):** `$schema`, `plugins`, `react/rules-of-hooks`, `react/only-export-components`, `React Compiler` (+102 more)
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 121 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **2 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `react` connect `App.tsx` to `package.json`?**
  _High betweenness centrality (0.033) - this node is a cross-community bridge._
- **Why does `devDependencies` connect `devDependencies` to `package.json`?**
  _High betweenness centrality (0.026) - this node is a cross-community bridge._
- **Why does `dependencies` connect `dependencies` to `package.json`?**
  _High betweenness centrality (0.021) - this node is a cross-community bridge._
- **What connects `$schema`, `plugins`, `react/rules-of-hooks` to the rest of the system?**
  _107 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `Google Earth Engine Preprocessing Pipeline` be split into smaller, more focused modules?**
  _Cohesion score 0.11428571428571428 - nodes in this community are weakly interconnected._
- **Should `App.tsx` be split into smaller, more focused modules?**
  _Cohesion score 0.1251778093883357 - nodes in this community are weakly interconnected._
- **Should `🔄 The Standard Parallel Git Lifecycle` be split into smaller, more focused modules?**
  _Cohesion score 0.14285714285714285 - nodes in this community are weakly interconnected._