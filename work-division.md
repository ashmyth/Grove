# Team Work Breakdown & Implementation Plan — Grove (GeoPrithvi-Agri)

**Project Title:** AI-Driven Automated Crop Mapping, Stage-Wise Moisture Stress Detection, and 8-Day Canal Command Irrigation Advisory System  
**Document Purpose:** Clear technical demarcation of tasks, file ownership, and interface contracts for a 3-person engineering team.

---

## 1. Architectural Responsibility Matrix

```
                       ┌──────────────────────────────────────────────┐
                       │          GROVE PROJECT REPOSITORY            │
                       └──────────────────────┬───────────────────────┘
                                              │
         ┌────────────────────────────────────┼────────────────────────────────────┐
         ▼                                    ▼                                    ▼
┌───────────────────────────────┐ ┌───────────────────────────────┐ ┌───────────────────────────────┐
│           PERSON 1            │ │           PERSON 2            │ │           PERSON 3            │
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

---

## 2. Detailed Role & Task Breakdown

### 🛰️ Person 1: Remote Sensing & Data Pipeline Engineer
* **Primary Scope:** Cloud-native satellite preprocessing on Google Earth Engine, radar/optical physics, and local raster streaming.
* **Primary Files Owned:**
  - `backend/gee_pipeline.py`
  - `backend/data_loader.py`
  - `data/` (Sample GeoTIFFs, boundary GeoJSONs, shapefiles)

#### Core Deliverables & Tasks:
1. **Google Earth Engine (GEE) Ingestion Pipeline (`backend/gee_pipeline.py`)**:
   - Authenticate with GEE Python API and clip satellite scenes to canal command boundaries.
   - **Sentinel-2 MSI (Optical):** Apply Scene Classification Layer (SCL) cloud and cloud-shadow masking; calculate NDVI, EVI, and NDWI.
   - **Sentinel-1 GRD (SAR):** Calibrate to Sigma Nought ($\sigma^\circ\text{ dB}$); implement a $7\times 7$ directional Refined Lee speckle filter.
   - **SAR Polarimetric Decomposition:** Compute volume scattering ($m_v$) and surface scattering ($m_s$) indicators.
   - **Landsat-8 TIRS (Thermal):** Compute Land Surface Temperature (LST) from Band 10 and determine 30-day thermal anomaly baselines.
   - **ECMWF ERA5-Land (Meteorology):** Sample daily $T_{\min}, T_{\max}$, rainfall, and solar radiation ($R_a$).
   - Export 10m resampled 12-channel GeoTIFF composite chips.
2. **High-Performance Memory-Mapped Data Loader (`backend/data_loader.py`)**:
   - Implement windowed raster chunking via `rasterio` and `numpy.memmap` to restrict peak memory usage below 3.5 GB.
   - Construct PyTorch-ready `Dataset` and `DataLoader` classes emitting optical temporal sequence tensors `(B, T, 6, H, W)` and SAR spatial patch tensors `(B, 2, 11, 11)`.
3. **Mock Data Generation (`data/`)**:
   - Generate synthetic sample GeoTIFF files and canal boundary GeoJSONs so Person 2 and Person 3 can develop without blocking on real GEE API credentials.

---

### 🧠 Person 2: AI/ML Core & Satellite Hydrology Engineer
* **Primary Scope:** Geospatial foundation models, multimodal late-fusion, signal processing, and hydrological water balance modeling.
* **Primary Files Owned:**
  - `backend/model.py`
  - `backend/stress.py`
  - `backend/hydrology.py`
  - `tests/test_model.py`
  - `tests/test_hydrology.py`

#### Core Deliverables & Tasks:
1. **Multimodal Deep Learning Backbone (`backend/model.py`)**:
   - **Optical Branch:** Load `ibm-nasa-geospatial/Prithvi-100M` from Hugging Face as a frozen feature extractor yielding 256-dimensional embeddings ($f_{\text{optical}} \in \mathbb{R}^{256}$).
   - **SAR Branch:** Implement a 2D CNN patch encoder with residual blocks processing $11\times 11$ radar patches ($f_{\text{SAR}} \in \mathbb{R}^{256}$).
   - **Late Fusion (`MSF-Net`):** Implement vector addition $f_{\text{fused}} = f_{\text{optical}} \oplus f_{\text{SAR}}$ with an MLP classification head.
   - **Auxiliary Loss Regularization:** Multi-task loss heads ($\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{fused}} + 0.3\mathcal{L}_{\text{opt}} + 0.3\mathcal{L}_{\text{sar}}$) enabling automated fallback to SAR predictions during optical cloud cover.
   - **Zero-GPU Fallback:** Implement Scikit-Learn Random Forest Classifier ($N_{\text{trees}}=100$) for CPU-only execution.
2. **Phenology & Moisture Stress Engine (`backend/stress.py`)**:
   - Implement Region-Adaptive Phenology Alignment (RAM) with Savitzky-Golay polynomial smoothing (`scipy.signal.savgol_filter`).
   - Extract dynamic Start of Season (SOS), Peak, and Length of Growing Period (LGP) markers.
   - Implement Composite Moisture Stress Index (CMSI) dynamically weighting VCI, SAR Soil Moisture Index ($SMI_{\text{SAR}}$), and Thermal Anomaly Index ($TAI_{\text{LST}}$).
3. **Hydrological Water Deficit Engine (`backend/hydrology.py`)**:
   - Implement the Hargreaves-Samani Reference Evapotranspiration ($ET_o$) model with solar radiation geometry ($R_a$).
   - Calculate stage-specific crop water demand ($ET_c = K_c \times ET_o$) across vegetative, flowering, and maturity stages.
   - Compute effective rainfall ($P_{\text{eff}} = 0.8 \times P_{\text{total}}$).
   - Formulate 8-day net volumetric deficit ($m^3/\text{ha}$ and $mm$) and calculate required sluice discharge rates ($Q = V / t$).
4. **Unit & Math Testing (`tests/`)**:
   - Write test suites validating tensor dimensions and hydrological formulas against FAO-56 benchmark tables.

---

### 💻 Person 3: Full-Stack Developer (FastAPI + React Frontend)
* **Primary Scope:** Asynchronous REST endpoints, interactive WebGL/Leaflet GIS mapping, data visualization, and client-side UI/UX.
* **Primary Files Owned:**
  - `backend/main.py`
  - `frontend/package.json`
  - `frontend/vite.config.ts`
  - `frontend/src/*` (Components, hooks, map viewers, tables, charts)

#### Core Deliverables & Tasks:
1. **FastAPI REST API Service (`backend/main.py`)**:
   - Define Pydantic request/response validation schemas.
   - Build `GET /api/v1/crops/geojson`: Serves 10m vectorized crop classification parcel boundaries.
   - Build `GET /api/v1/stress/tiles/{z}/{x}/{y}.png`: Dynamic XYZ map tile server rendering moisture stress heatmaps.
   - Build `GET /api/v1/canals/advisories`: Delivers 8-day volumetric water deficits ($m^3/\text{ha}$) and sluice discharge rates ($Q = V / t$).
   - Build `GET /api/v1/pixel/timeseries?lat={lat}&lon={lon}`: Returns raw and Savitzky-Golay smoothed NDVI, $SMI_{\text{SAR}}$, and LST temporal profiles.
2. **React 18/19 + Vite Frontend Application (`frontend/`)**:
   - Setup project structure with TypeScript, Vite, TailwindCSS, and Lucide Icons.
   - **`MapViewer.tsx`**: Interactive dual-layer WebGL / Leaflet GIS map with layer toggling (10m Crop Boundaries vs. Stage Moisture Stress Heatmap) and click-to-inspect parcel coordinates.
   - **`CanalAdvisory.tsx`**: Canal command block data table with status indicators (Normal, Alert, Critical) and sluice discharge release cards.
   - **`PhenologyChart.tsx`**: Interactive Recharts time-series chart showing seasonal crop growth curves and moisture stress anomalies.
   - **`ExportAdvisory.tsx`**: Client-side CSV/PDF export of irrigation release schedules.
3. **Dev Environment & Integration**:
   - Setup Vite proxy routing `/api/*` to FastAPI on port 8000.
   - Add root npm/Python run scripts for simultaneous local development.

---

## 3. Interface Contracts Between Teammates

These strict contracts allow each person to work independently with mock data without blocking each other:

### Interface A: Person 1 ➡️ Person 2 (Data to ML/Hydrology)
* **Contract:** `data_loader.py` exposes:
  ```python
  def get_crop_tensors(sample_id: str) -> Tuple[torch.Tensor, torch.Tensor, dict]:
      # optical_tensor: torch.Tensor of shape (B, T=3, C=6, H=224, W=224)
      # sar_patch:      torch.Tensor of shape (B, C=2, H=11, W=11)
      # metadata:       {"crs": str, "bounds": tuple, "parcel_ids": list}
  ```

### Interface B: Person 2 ➡️ Person 3 (ML/Hydrology to Backend API)
* **Contract:** `model.py` and `hydrology.py` expose:
  ```python
  def predict_crop_classes(optical: torch.Tensor, sar: torch.Tensor) -> np.ndarray:
      # Returns (N,) class integers: 0=Paddy, 1=Cotton, 2=Maize, 3=Sugarcane, 4=Pulses
      
  def compute_canal_advisories(block_id: str, area_ha: float) -> dict:
      # Returns:
      # {
      #     "block_id": str,
      #     "deficit_mm": float,
      #     "volume_m3": float,
      #     "recommended_discharge_cumecs": float,
      #     "stress_level": "Normal" | "Mild" | "Moderate" | "Severe"
      # }
  ```

### Interface C: Person 3 Backend ➡️ Person 3 Frontend (API to React)
* **Contract:** Standard JSON & GeoJSON payloads:
  - `GET /api/v1/canals/advisories` ➡️ `Array<{ id, block_name, crop_type, deficit_m3_ha, discharge_m3s, status }>`
  - `GET /api/v1/pixel/timeseries` ➡️ `{ dates: string[], ndvi_raw: number[], ndvi_smoothed: number[], smi_sar: number[], lst_anomaly: number[] }`

---

## 4. Development Workflow & Git Rules

1. **Trunk-Based Development:**
   - Feature branches: `feature/person1-data-pipeline`, `feature/person2-ml-hydrology`, `feature/person3-react-api`.
   - Keep pull requests small and focused on assigned modules.
2. **Knowledge Graph Synchronization:**
   - After creating or editing code files, run `python -m graphify update .` to ensure the project architecture map stays up to date.
3. **Pre-Commit Hygiene:**
   - Verify tests pass with `pytest`.
   - Never commit raw GeoTIFF rasters or credentials (`.gitignore` is pre-configured).
