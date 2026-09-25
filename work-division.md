# Team Work Breakdown & AI Agent Execution Guide — Grove (GeoPrithvi-Agri)

> **🤖 FOR AI CODING AGENTS (Cursor, Claude Code, Antigravity, Copilot, Codex, Aider):**  
> If the user tells you **"I am Teammate 1"**, **"I am Teammate 2"**, or **"I am Teammate 3"** (or Person 1 / 2 / 3), **YOU MUST ADOPT THAT PERSONA IMMEDIATELY**.  
> 1. Read your assigned section below.  
> 2. **STRICT SCOPE FENCE:** ONLY create or modify files in your **Owned Files** list. Do NOT touch, rename, or delete files owned by other teammates.  
> 3. Adhere strictly to the **Interface Contracts** in Section 4 so your code integrates seamlessly without breaking other teammates' branches.  
> 4. If an upstream module from another teammate is not yet implemented, use the provided **Mocking Strategy** rather than modifying their file.

---

## 1. Team Architectural Division & File Ownership

```
                       ┌──────────────────────────────────────────────┐
                       │          GROVE PROJECT REPOSITORY            │
                       └──────────────────────┬───────────────────────┘
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼                                    ▼                                    ▼
┌───────────────────────────────┐ ┌───────────────────────────────┐ ┌───────────────────────────────┐
│          TEAMMATE 1           │ │          TEAMMATE 2           │ │          TEAMMATE 3           │
│   Data Ingestion & Remote     │ │    AI/ML Model & Satellite    │ │    FastAPI REST Backend &     │
│       Sensing Pipeline        │ │       Hydrology Engine        │ │    React (TypeScript) Web     │
├───────────────────────────────┤ ├───────────────────────────────┤ ├───────────────────────────────┤
│ • GEE cloud preprocessing     │ │ • Prithvi-EO-100M ViT         │ │ • FastAPI REST endpoints      │
│ • S1 SAR speckle & polarimetry│ │ • SAR 2D CNN patch encoder    │ │ • Pydantic schemas            │
│ • S2 Optical & cloud masks    │ │ • MSF-Net late-fusion         │ │ • React + Vite UI layout      │
│ • L8 LST thermal inversion    │ │ • Random Forest fallback      │ │ • MapViewer GIS component     │
│ • ERA5 weather ingestion      │ │ • Savitzky-Golay phenology    │ │ • CanalAdvisory tables/gauges │
│ • Memory-mapped data loader   │ │ • CMSI multi-index stress     │ │ • Phenology Recharts chart    │
│ • Mock GeoTIFF / GeoJSON data │ │ • Hargreaves ET0 & FAO-56 Kc  │ │ • ExportAdvisory (PDF/CSV)    │
│ • Coordinate projections      │ │ • 8-day water deficit formula │ │ • Vite proxy & dev server     │
└───────────────────────────────┘ └───────────────────────────────┘ └───────────────────────────────┘
```

| Teammate | Role Title | Primary Owned Files & Folders |
| :--- | :--- | :--- |
| **Teammate 1** | Remote Sensing & Data Pipeline Engineer | `backend/gee_pipeline.py`, `backend/data_loader.py`, `data/` |
| **Teammate 2** | AI/ML Core & Satellite Hydrology Engineer | `backend/model.py`, `backend/stress.py`, `backend/hydrology.py`, `tests/` |
| **Teammate 3** | Full-Stack Developer (FastAPI + React) | `backend/main.py`, `frontend/` (all files in `frontend/*`) |

---

## 2. Agent Execution Guides by Teammate

---

### 🛰️ Teammate 1: Remote Sensing & Data Pipeline Engineer
> **Trigger Prompts:** `"I am Teammate 1"`, `"I am Person 1"`, `"Work on Teammate 1's tasks"`

#### 🎯 Agent Mission:
You are responsible for the Earth Observation data engineering lifecycle: fetching raw multi-spectral, microwave SAR, thermal, and meteorological data via Google Earth Engine, applying physics-based radiometric calibrations and speckle filters, and providing a memory-mapped PyTorch data loader.

#### 📂 Files You Own:
* `backend/gee_pipeline.py`
* `backend/data_loader.py`
* `data/` (Sample GeoTIFFs, boundary GeoJSONs, shapefiles)

#### 🚫 Scope Fence (DO NOT TOUCH):
* Do NOT edit `backend/model.py`, `backend/stress.py`, or `backend/hydrology.py` (Owned by Teammate 2).
* Do NOT edit `backend/main.py` or `frontend/` (Owned by Teammate 3).

#### 📋 Step-by-Step Implementation Checklist:
- [ ] **Step 1: GEE Cloud Pipeline (`backend/gee_pipeline.py`)**
  - Authenticate with `ee.Initialize()`. Support both service account key and interactive token authentication.
  - Clip all spatial image collections to the canal command boundary Polygon/MultiPolygon.
  - **Sentinel-2 MSI:** Apply Scene Classification Layer (SCL) cloud mask. Calculate NDVI, EVI, and NDWI.
  - **Sentinel-1 GRD:** Filter by IW mode and Ascending/Descending swaths. Calibrate to $\sigma^\circ\text{ (dB)}$. Apply a $7\times 7$ directional Refined Lee speckle filter.
  - **SAR Polarimetry:** Calculate volume scattering proxy $m_v = \frac{4\sigma^\circ_{\text{VH}}}{\sigma^\circ_{\text{VV}} + \sigma^\circ_{\text{VH}}}$ and surface scattering proxy $m_s = \frac{\sigma^\circ_{\text{VV}} - \sigma^\circ_{\text{VH}}}{\sigma^\circ_{\text{VV}} + \sigma^\circ_{\text{VH}}}$.
  - **Landsat-8 TIRS:** Compute Land Surface Temperature (LST) from Band 10 and compute 30-day thermal anomaly baselines.
  - **ERA5-Land:** Extract $2\text{m}$ $T_{\min}, T_{\max}$, daily precipitation $P_{\text{total}}$, and solar radiation $R_s$.
  - Export a 10m metric-aligned 12-channel GeoTIFF composite chip.
- [ ] **Step 2: Memory-Mapped Data Loader (`backend/data_loader.py`)**
  - Implement windowed reading via `rasterio` and `numpy.memmap` so regional GeoTIFFs load without exceeding 3.5 GB RAM.
  - Create a PyTorch `Dataset` that yields optical sequence tensors `(B, T=3, C=6, H=224, W=224)` and SAR patch tensors `(B, C=2, H=11, W=11)`.
- [ ] **Step 3: Synthetic / Mock Dataset (`data/`)**
  - Generate lightweight synthetic sample `.geotiff` and `.geojson` mock files so Teammate 2 and 3 can test locally immediately without GEE credentials.

---

### 🧠 Teammate 2: AI/ML Core & Satellite Hydrology Engineer
> **Trigger Prompts:** `"I am Teammate 2"`, `"I am Person 2"`, `"Work on Teammate 2's tasks"`

#### 🎯 Agent Mission:
You are responsible for the multimodal deep learning architecture and the satellite hydrology balance equations: loading the `Prithvi-EO-100M` geospatial foundation model, building the 2D CNN radar branch, implementing late-fusion with auxiliary loss fallbacks, and coding the Hargreaves $ET_o$ / FAO-56 stage-wise water deficit engine.

#### 📂 Files You Own:
* `backend/model.py`
* `backend/stress.py`
* `backend/hydrology.py`
* `tests/test_model.py`
* `tests/test_hydrology.py`

#### 🚫 Scope Fence (DO NOT TOUCH):
* Do NOT edit `backend/gee_pipeline.py` or `backend/data_loader.py` (Owned by Teammate 1).
* Do NOT edit `backend/main.py` or `frontend/` (Owned by Teammate 3).

#### 📋 Step-by-Step Implementation Checklist:
- [ ] **Step 1: Multimodal Deep Learning Backbone (`backend/model.py`)**
  - Load `ibm-nasa-geospatial/Prithvi-100M` via Hugging Face `transformers` with frozen weights to produce 256-dim embeddings ($f_{\text{optical}} \in \mathbb{R}^{256}$).
  - Build a 2D CNN encoder with residual conv blocks processing $11\times 11$ SAR patches ($f_{\text{SAR}} \in \mathbb{R}^{256}$).
  - Implement `MSFNetCropClassifier`: late-fusion vector addition $f_{\text{fused}} = f_{\text{optical}} \oplus f_{\text{SAR}}$ with MLP head (`Linear(256, 128) -> ReLU -> Dropout(0.3) -> Linear(128, num_crops)`).
  - Implement auxiliary loss heads ($\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{fused}} + 0.3\mathcal{L}_{\text{opt}} + 0.3\mathcal{L}_{\text{sar}}$) with automated fallback to SAR when optical cloud mask $\ge 80\%$.
  - Implement `RandomForestCropClassifier` fallback using `scikit-learn` for CPU environments.
- [ ] **Step 2: Dynamic Phenology & Stress Engine (`backend/stress.py`)**
  - Implement Region-Adaptive Phenology Alignment (RAM) with Savitzky-Golay polynomial smoothing (`scipy.signal.savgol_filter`).
  - Extract Start of Season (SOS), Peak Vegetative, and Length of Growing Period (LGP).
  - Implement Composite Moisture Stress Index:
    $$\text{CMSI} = w_{\text{VCI}}(100 - \text{VCI}) + w_{\text{SMI}}(100 - SMI_{\text{SAR}}) + w_{\text{TAI}}\cdot\text{Clip}(TAI_{\text{LST}} \times 20, 0, 100)$$
    with stage-dependent weights (Vegetative: 0.2/0.6/0.2, Flowering: 0.35/0.35/0.30, Ripening: 0.5/0.3/0.2).
- [ ] **Step 3: Hydrological Deficit Engine (`backend/hydrology.py`)**
  - Implement Hargreaves-Samani Reference Evapotranspiration:
    $$ET_o = 0.0023 \times (T_{\text{avg}} + 17.8) \times (T_{\max} - T_{\min})^{0.5} \times \frac{R_a}{2.45}$$
  - Implement FAO-56 stage-wise crop evapotranspiration ($ET_c = K_c \times ET_o$).
  - Implement effective rainfall ($P_{\text{eff}} = 0.8 \times P_{\text{total}} - 5$ for $P_{\text{total}} > 10\text{ mm}$).
  - Compute net 8-day water deficit: $\text{Deficit}_8 = \max(0, \sum (ET_c - ET_a - P_{\text{eff}}))$.
  - Compute volumetric requirement ($V = \text{Deficit}_8 \times 10 \times A$) and sluice discharge ($Q = \frac{V}{t \times 3600 \times 0.70}$).
- [ ] **Step 4: Automated Unit Tests (`tests/`)**
  - Write test cases in `tests/test_model.py` (tensor dimensions, cloud fallback) and `tests/test_hydrology.py` (verifying equations against standard FAO-56 reference values).

---

### 💻 Teammate 3: Full-Stack Developer (FastAPI + React Frontend)
> **Trigger Prompts:** `"I am Teammate 3"`, `"I am Person 3"`, `"Work on Teammate 3's tasks"`

#### 🎯 Agent Mission:
You are responsible for the entire user-facing stack: building the FastAPI asynchronous REST endpoints, creating Pydantic schemas, and constructing the modern React 18/19 + Vite web application with interactive GIS map layers, canal command tables, time-series charts, and export tools.

#### 📂 Files You Own:
* `backend/main.py`
* `frontend/` (Everything inside `frontend/*`: `package.json`, `vite.config.ts`, `src/App.tsx`, `src/components/*`, `src/services/*`)

#### 🚫 Scope Fence (DO NOT TOUCH):
* Do NOT edit `backend/gee_pipeline.py` or `backend/data_loader.py` (Owned by Teammate 1).
* Do NOT edit `backend/model.py`, `backend/stress.py`, or `backend/hydrology.py` (Owned by Teammate 2).

#### 📋 Step-by-Step Implementation Checklist:
- [ ] **Step 1: FastAPI REST Service (`backend/main.py`)**
  - Setup FastAPI app with CORS middleware enabled for `http://localhost:5173` (Vite dev server).
  - Implement `GET /api/v1/health`: Returns API and GPU runtime status.
  - Implement `GET /api/v1/crops/geojson`: Serves 10m vectorized crop classification polygon layers.
  - Implement `GET /api/v1/stress/tiles/{z}/{x}/{y}.png`: Dynamic XYZ map tile endpoint serving color-coded moisture stress heatmaps.
  - Implement `GET /api/v1/canals/advisories`: Returns list of canal blocks with 8-day water deficit ($m^3/\text{ha}$), current crop stage, and recommended sluice discharge ($m^3/s$).
  - Implement `GET /api/v1/pixel/timeseries?lat={lat}&lon={lon}`: Delivers raw and smoothed NDVI, $SMI_{\text{SAR}}$, and LST temporal profiles for pixel click drilldown.
  - *(Note: If Teammate 2 has not finished `model.py` or `hydrology.py`, return realistic mock JSON based on Section 3 contracts).*
- [ ] **Step 2: React Frontend Initialization (`frontend/`)**
  - Initialize React 18+ with TypeScript and Vite.
  - Install dependencies: `react-leaflet` / `maplibre-gl`, `lucide-react`, `recharts`, `axios`, `tailwindcss`.
  - Configure `vite.config.ts` to proxy `/api` requests to `http://localhost:8000`.
- [ ] **Step 3: Component Architecture (`frontend/src/components/`)**
  - **`MapViewer.tsx`**: Interactive dual-layer GIS map with layer switcher:
    - Layer A: 10m Crop Classification Boundaries.
    - Layer B: Stage Moisture Stress Heatmap (Green=No Stress, Yellow=Mild, Orange=Moderate, Red=Severe).
    - Add click listener to fetch pixel time-series on coordinates.
  - **`CanalAdvisory.tsx`**: Responsive table listing canal distributaries, crop stages, net water deficits ($m^3/\text{ha}$), status pills, and discharge gauges ($Q = V / t$).
  - **`PhenologyChart.tsx`**: Interactive Recharts graph plotting Savitzky-Golay smoothed NDVI curves, radar moisture, and thermal anomalies over time.
  - **`ExportAdvisory.tsx`**: Client-side CSV/PDF export of irrigation advisories for field operators.
- [ ] **Step 4: Layout & Dev Scripts**
  - Wire components into a responsive layout in `App.tsx`.
  - Provide root dev script (e.g. `npm run dev`) that boots Vite and runs alongside Uvicorn.

---

## 3. Strict Interface Contracts Between Teammates

### Interface 1: Data Pipeline ➡️ ML / Hydrology (Teammate 1 ➡️ Teammate 2)
In `backend/data_loader.py`, Teammate 1 must implement:
```python
def load_feature_tensors(sample_id: str) -> dict:
    """
    Returns:
        {
            "optical_tensor": torch.Tensor, # Shape: (B, T=3, C=6, H=224, W=224)
            "sar_patch":      torch.Tensor, # Shape: (B, C=2, H=11, W=11)
            "dem_slope":      np.ndarray,   # Shape: (H, W)
            "era5_meteo":     dict,         # {"t_min": float, "t_max": float, "p_total": float, "ra": float}
            "metadata":       dict          # {"crs": "EPSG:32643", "bounds": [...], "dates": [...]}
        }
    """
```

### Interface 2: ML / Hydrology ➡️ FastAPI Backend (Teammate 2 ➡️ Teammate 3)
In `backend/model.py` and `backend/hydrology.py`, Teammate 2 must implement:
```python
def run_crop_inference(optical_tensor: torch.Tensor, sar_patch: torch.Tensor) -> np.ndarray:
    """Returns 2D integer array (H, W) where 0=Paddy, 1=Cotton, 2=Maize, 3=Sugarcane, 4=Pulses"""

def compute_block_water_deficit(block_id: str, area_ha: float, crop_type: str, stage: str) -> dict:
    """
    Returns:
        {
            "block_id": str,
            "crop_type": str,
            "stage": "Vegetative" | "Flowering" | "Ripening",
            "deficit_mm": float,
            "volumetric_deficit_m3": float,
            "recommended_discharge_cumecs": float,
            "stress_category": "Normal" | "Mild" | "Moderate" | "Severe"
        }
    """
```

### Interface 3: FastAPI Backend ➡️ React Frontend (Teammate 3 Backend ➡️ Frontend)
In `frontend/src/services/api.ts`, Teammate 3 consumes:
```typescript
export interface CanalAdvisoryItem {
  id: string;
  block_name: string;
  reach: "head" | "middle" | "tail";
  crop_type: string;
  stage: string;
  deficit_m3_ha: number;
  discharge_cumecs: number;
  stress_level: "Normal" | "Mild" | "Moderate" | "Severe";
}

export interface PixelTimeseriesData {
  dates: string[];
  doy: number[];
  ndvi_raw: number[];
  ndvi_smoothed: number[];
  smi_sar: number[];
  lst_anomaly: number[];
}
```

---

## 4. Git Parallel Workflow & Collaboration Rules

To ensure 100% isolation and avoid code collisions or merge conflicts when working simultaneously:

### 🔄 The Standard Parallel Git Lifecycle

```
main (protected baseline)
  │
  ├──► git checkout -b feature/t1-data-pipeline ──► work ──► PR #1 ──► merge to main
  │
  ├──► git checkout -b feature/t2-ml-hydrology ──► work ──► PR #2 ──► merge to main
  │
  └──► git checkout -b feature/t3-react-fastapi ──► work ──► PR #3 ──► merge to main
```

#### Step 1: Starting Your Task
Always create your isolated feature branch from the latest `main`:
```bash
git checkout main
git pull origin main

# Teammate 1:
git checkout -b feature/t1-data-pipeline

# Teammate 2:
git checkout -b feature/t2-ml-hydrology

# Teammate 3:
git checkout -b feature/t3-react-fastapi
```

#### Step 2: Committing Your Work
Make small, frequent commits using conventional commit syntax:
- Teammate 1: `git commit -m "feat(data): implement GEE cloud masking and speckle filter"`
- Teammate 2: `git commit -m "feat(ml): implement Prithvi ViT and Hargreaves ET0 engine"`
- Teammate 3: `git commit -m "feat(ui): implement CanalAdvisory table and Leaflet MapViewer"`

#### Step 3: Keeping Up to Date with Teammates (Syncing)
When another teammate merges their feature into `main`, rebase or merge `main` into your branch:
```bash
git fetch origin
git merge origin/main
```
Because of the **strict disjoint file ownership** (Teammate 1, 2, and 3 touch zero shared files), Git will cleanly merge changes without conflicts!

#### Step 4: Knowledge Graph Update
Whenever you add or modify code, run Graphify to update the AST graph:
```bash
python -m graphify update .
```

#### Step 5: Pull Request & Merge
1. Push your branch to GitHub:
   ```bash
   git push -u origin <your-branch-name>
   ```
2. Open a Pull Request into `main`.
3. Verify that your tests pass (`pytest tests/`).
4. Merge into `main`. Clean up local branch:
   ```bash
   git checkout main
   git pull origin main
   git branch -d <your-branch-name>
   ```

