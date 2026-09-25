# Technical Architecture & System Specification: Grove (GeoPrithvi-Agri)

**System Name:** Grove / GeoPrithvi-Agri  
**Sub-Title:** AI-Driven Automated Crop Mapping, Stage-Wise Moisture Stress Detection, and 8-Day Canal Command Irrigation Advisory System  
**Version:** 1.0.0-rc1  
**Classification:** Production Engineering Specification  

---

## 1. System Overview & Architectural Topology

Grove couples Cloud-native Earth Observation (EO) preprocessing on Google Earth Engine with a lightweight edge/consumer-grade multimodal deep learning and satellite hydrology pipeline.

```
                              [GOOGLE EARTH ENGINE CLOUD INFRASTRUCTURE]
       Sentinel-2 (MSI)         Sentinel-1 (SAR C-Band)      Landsat-8 (TIRS)          ERA5-Land
     (B2,B3,B4,B8,B11,B12)          (VV + VH GRD)               (Band 10)         (Tmin, Tmax, Precip)
              │                           │                          │                      │
       Cloud-Masking (SCL)       Refined Lee Speckle         Split-Window LST       Daily Insolation (Ra)
       Indices (NDVI,EVI,NDWI)   Polarimetric Decomp (mv,ms) Thermal Anomaly         Effective Precip (Peff)
              └───────────────┬───────────┴──────────────────────────┴──────────────────────┘
                              ▼
           [GEOTIFF EXPORT / LOCAL INGESTION PIPELINE]
                     (10m Resampled Metric Grid)
                              │
          ┌───────────────────┴────────────────────────┐
          ▼                                            ▼
   [DEEP LEARNING PIPELINE]                   [HYDROLOGICAL ENGINE]
┌──────────────────────────────────────┐     ┌──────────────────────────────────────┐
│ Branch A: Prithvi-EO-100M ViT       │     │ Hargreaves-Samani ET0 Equation       │
│  - Frozen 100M MAE Backbone (NASA)   │     │  - Extraterrestrial Radiation (Ra)   │
│  - Multi-Temporal Optical Embeddings │     │  - 8-Day Rolling Potential ET        │
│                                      │     │                                      │
│ Branch B: 2D CNN Radar Branch        │     │ FAO-56 Dynamic Crop Coefficients     │
│  - 11x11 Spatial SAR Patch Encoder   │     │  - Kc linked to Phenology Stage      │
│  - Residual Conv2D Blocks            │     │  - Crop Water Demand: ETc = Kc * ET0 │
│                                      │     │                                      │
│ Asymmetric Late-Fusion (MSF-Net)     │     │ Multi-Index Moisture Stress          │
│  - Vector Addition: f_opt ⊕ f_sar    │     │  - VCI (Vegetation Condition)        │
│  - Multi-Task Auxiliary Loss Heads   │     │  - SMI_SAR (Soil Moisture Index)     │
│  - Cloud-Occlusion SAR Fallback      │     │  - Thermal Anomaly (LST Deviation)   │
│                                      │     │                                      │
│ Zero-GPU Fallback: Random Forest     │     │ 8-Day Volumetric Water Deficit       │
│  - 100 Estimators, Multi-Temp Input  │     │  - Deficit = ETc - ETa - Peff        │
└──────────────────┬───────────────────┘     │  - Volumetric: m³/ha & mm depth      │
                   │                         └──────────────────┬───────────────────┘
                   └─────────────────┬──────────────────────────┘
                                     ▼
                        [FASTAPI ASYNC REST BACKEND]
     /api/crops (GeoJSON) | /api/stress (COG/Tiles) | /api/advisories | /api/phenology
                                     │
                                     ▼
                   [REACT INTERACTIVE WEB APPLICATION]
        ├── Interactive WebGL/Leaflet Geospatial Map (10m Crop & Stress Boundaries)
        ├── Stage-Wise Moisture Stress Categorization (None, Mild, Moderate, Severe)
        ├── Canal Command Block Aggregated Sluice Release Table & Gauges (Q = V / t)
        └── Dynamic Pixel-Level Phenological Curve Inspector (Recharts / Canvas)
```

---

## 2. Technology Stack

| Layer | Component | Selection & Version | Rationale & Technical Role |
| :--- | :--- | :--- | :--- |
| **Cloud EO Preprocessing** | Remote Sensing Engine | **Google Earth Engine (GEE)** `earthengine-api >= 0.1.370` | Eliminates raw multi-gigabyte satellite imagery downloads; executes cloud masking, radiometric calibration, and spatial resampling on Google Cloud infrastructure. |
| **Deep Learning** | Tensor Framework | **PyTorch >= 2.1.0** (CUDA 11.8/12.1 or CPU) | Powers the `Prithvi-EO-100M` Vision Transformer, radar 2D CNN patch branch, and late-fusion layers. |
| **Foundation Backbone** | Geospatial ViT | **`Prithvi-EO-1.0-100M` (NASA/IBM)** via HuggingFace `transformers >= 4.36.0` | State-of-the-art 100M parameter Masked Autoencoder pretrained on 4.2M HLS multi-temporal image chips; frozen to allow fast inference on standard GPUs/CPUs. |
| **Zero-GPU Fallback** | Classical ML | **Scikit-Learn >= 1.3.0** | Random Forest Classifier ($N_{\text{trees}}=100$) providing sub-second inference when GPU acceleration or deep learning dependencies are unavailable. |
| **Raster & Array I/O** | Geospatial Array Processing | **Rasterio >= 1.3.8**, **GDAL >= 3.6.0**, **NumPy >= 1.24.0** | Handles memory-mapped windowed reads (`numpy.memmap`) of regional GeoTIFFs to prevent Out-Of-Memory (OOM) errors. |
| **Vector & GIS** | Vector Topologies | **GeoPandas >= 0.14.0**, **Shapely >= 2.0.0** | Parses canal command boundary polygons, distributary reach shapes, and field parcels; performs high-speed spatial joins. |
| **Time-Series & Signal** | Signal Processing | **SciPy >= 1.11.0** (`scipy.signal.savgol_filter`) | Fits dynamic Savitzky-Golay polynomial filters on temporal NDVI vectors for Region-Adaptive Phenology Alignment (RAM). |
| **Backend REST API** | High-Performance Server | **FastAPI >= 0.109.0**, **Uvicorn >= 0.27.0**, **Pydantic v2** | High-throughput asynchronous REST API serving GeoJSON vector boundaries, raster tile endpoints, and JSON advisory payloads. |
| **Frontend Framework** | Client User Interface | **React 18/19**, **TypeScript >= 5.0**, **Vite >= 5.0** | Responsive, component-driven client architecture; zero full-page reloads, rich client-side caching, and modern UX state management. |
| **Geospatial Map UI** | Interactive Web Map | **MapLibre GL JS >= 3.6.0** / **React-Leaflet >= 4.2.0** | GPU-accelerated raster and vector tiling for 10m parcel boundaries, stress overlays, and interactive parcel click handlers. |
| **Data Visualization** | Scientific Charts | **Recharts >= 2.10.0** / **Chart.js** | Client-side responsive charts for Savitzky-Golay smoothed NDVI trajectories, SAR soil moisture index, and LST anomaly curves. |

---

## 3. Multi-Source Remote Sensing & Data Pipeline

Grove synchronizes four distinct satellite sensors and meteorological grids at a standardized **10m spatial resolution** on a common UTM grid projection:

### 3.1 Optical Remote Sensing (Sentinel-2 MSI / Landsat HLS)
* **Ingested Bands:** Blue (B2), Green (B3), Red (B4), Near-Infrared (B8), Shortwave Infrared 1 (B11), Shortwave Infrared 2 (B12).
* **Cloud Masking:** Uses Sentinel-2 Scene Classification Layer (SCL). Pixels flagged as cloud shadow (code 3), cloud medium probability (code 8), cloud high probability (code 9), or cirrus (code 10) are masked to `NaN`.
* **Computed Spectral Indices:**
  * Normalized Difference Vegetation Index:
    $$\text{NDVI} = \frac{\text{B8} - \text{B4}}{\text{B8} + \text{B4}}$$
  * Enhanced Vegetation Index:
    $$\text{EVI} = 2.5 \times \frac{\text{B8} - \text{B4}}{\text{B8} + 6.0 \times \text{B4} - 7.5 \times \text{B2} + 1.0}$$
  * Normalized Difference Water Index:
    $$\text{NDWI} = \frac{\text{B8} - \text{B11}}{\text{B8} + \text{B11}}$$

### 3.2 Synthetic Aperture Radar (Sentinel-1 C-Band GRD)
* **Configuration:** Level-1 Ground Range Detected (GRD), Interferometric Wide (IW) swath mode, Dual-polarization ($\text{VV} + \text{VH}$), $10\text{m}$ pixel spacing.
* **Radiometric Calibration:** Converts raw Digital Numbers (DN) to Sigma Nought backscattering coefficients in decibels:
  $$\sigma^\circ\,(\text{dB}) = 10 \cdot \log_{10}(\text{DN}^2) + C$$
* **Refined Lee Speckle Filtering:** Applied using a $7 \times 7$ moving directional adaptive window. It calculates local directional gradients, identifies homogeneous sub-windows, and smooths speckle noise while preserving field parcel boundaries:
  $$\hat{I} = \bar{I} + W \cdot (I - \bar{I})$$
  where the weighting factor $W$ is:
  $$W = \frac{\text{Var}(I) - \bar{I}^2 \cdot \sigma_v^2}{\text{Var}(I) \cdot (1 + \sigma_v^2)}$$
* **Dual-Polarization Polarimetric Proxies:**
  * **Volume Scattering Proxy ($m_v$):**
    $$m_v = \frac{4 \cdot \sigma^\circ_{\text{VH}}}{\sigma^\circ_{\text{VV}} + \sigma^\circ_{\text{VH}}}$$
    *(High correlation with canopy closure, stem branching, and crop biomass).*
  * **Surface Scattering Proxy ($m_s$):**
    $$m_s = \frac{\sigma^\circ_{\text{VV}} - \sigma^\circ_{\text{VH}}}{\sigma^\circ_{\text{VV}} + \sigma^\circ_{\text{VH}}}$$
    *(High correlation with topsoil dielectric permittivity and surface moisture).*

### 3.3 Thermal Infrared (Landsat-8 TIRS Band 10)
* **Resolution:** $100\text{m}$ native resampled to $10\text{m}$ via bicubic spline interpolation matched to the Sentinel grid.
* **Land Surface Temperature (LST) Calculation:**
  $$T_B = \frac{K_2}{\ln\left(\frac{K_1}{L_\lambda} + 1\right)}$$
  $$\text{LST} = \frac{T_B}{1 + \left(\lambda \cdot \frac{T_B}{\rho}\right) \cdot \ln(\epsilon)}$$
  where $\lambda = 10.895\,\mu\text{m}$, $\rho = \frac{h \cdot c}{\sigma} = 1.4388 \times 10^{-2}\,\text{m}\cdot\text{K}$, and $\epsilon$ is fractional vegetation cover emissivity derived from NDVI.

### 3.4 Meteorological Reanalysis (ECMWF ERA5-Land)
* **Gridded Parameters ($0.1^\circ$ spatial grid):**
  * $2\text{m}$ Minimum Daily Air Temperature ($T_{\min},\,^\circ\text{C}$)
  * $2\text{m}$ Maximum Daily Air Temperature ($T_{\max},\,^\circ\text{C}$)
  * Total Daily Precipitation ($P_{\text{total}},\,\text{mm}$)
  * Downwelling Solar Radiation ($R_s,\,\text{MJ}/\text{m}^2/\text{day}$)

---

## 4. Core AI/ML Frameworks & Neural Architectures

### 4.1 Geospatial Foundation Model (`Prithvi-EO-1.0-100M`)
`Prithvi-EO-1.0-100M` is a Vision Transformer based on the Masked Autoencoder (MAE) self-supervised framework trained on 4.2 million multi-temporal Harmonized Landsat-Sentinel (HLS) scenes.

```
Multi-Temporal Optical Tensor: (B, T=3, C=6, H=224, W=224)
                           │
                           ▼
             Patch Embedding (16 x 16 x 6)
                           │
                           ▼
          Spatial + Temporal Position Encodings
                           │
                           ▼
           12-Layer ViT Encoder (100M Params)
         [FROZEN WEIGHTS - ZERO GRADIENT UPDATE]
                           │
                           ▼
             Global Average Pooling (GAP)
                           │
                           ▼
          256-Dimensional Latent Embedding f_optical
```

* **Feature Extractor Head:**
  ```python
  class PrithviFeatureExtractor(nn.Module):
      def __init__(self, pretrained_model_name="ibm-nasa-geospatial/Prithvi-100M"):
          super().__init__()
          self.backbone = AutoModel.from_pretrained(pretrained_model_name)
          for param in self.backbone.parameters():
              param.requires_grad = False  # Freeze 100M backbone
          self.proj = nn.Linear(768, 256)
          
      def forward(self, x):
          # x: (B, T, C, H, W)
          features = self.backbone(x).last_hidden_state  # (B, SeqLen, 768)
          pooled = torch.mean(features, dim=1)           # (B, 768)
          return F.relu(self.proj(pooled))               # (B, 256)
  ```

### 4.2 SAR Structural Branch (2D CNN Spatial Patch Encoder)
Processes $11 \times 11$ pixel spatial patches of Sentinel-1 dual-polarization ($\text{VV}, \text{VH}$) data centered on the target parcel to extract micro-texture, roughness, and dielectric gradients.

```
Input SAR Patch: (B, 2, 11, 11)
  │
  ├── Conv2D(2, 64, kernel=3, padding=1) + BatchNorm2D + LeakyReLU
  ├── ResidualBlock(64 -> 64)
  ├── Conv2D(64, 128, kernel=3, stride=2, padding=1) + BatchNorm2D + LeakyReLU
  ├── ResidualBlock(128 -> 128)
  ├── AdaptiveAvgPool2d((1, 1))
  └── Linear(128, 256) -> f_SAR ∈ ℝ^256
```

### 4.3 Asymmetric Multimodal Late-Fusion Network (`MSF-Net`)
Fuses the 256-dimensional optical ViT vector and the 256-dimensional radar CNN vector via element-wise addition:
$$f_{\text{fused}} = f_{\text{optical}} \oplus f_{\text{SAR}} \in \mathbb{R}^{256}$$

The classification decision is computed via a Multi-Layer Perceptron (MLP):
$$\hat{y}_{\text{fused}} = \text{Softmax}\Big(\mathbf{W}_2 \cdot \text{Dropout}_{0.3}\big(\text{ReLU}(\mathbf{W}_1 \cdot f_{\text{fused}} + b_1)\big) + b_2\Big)$$

#### Auxiliary Loss Regularization:
To guarantee robustness during heavy monsoon cloud cover when optical data is missing or corrupted, the network incorporates branch-specific auxiliary classifiers:
$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{CE}}(\hat{y}_{\text{fused}}, y) + \lambda_{\text{opt}}\mathcal{L}_{\text{CE}}(\hat{y}_{\text{optical}}, y) + \lambda_{\text{sar}}\mathcal{L}_{\text{CE}}(\hat{y}_{\text{SAR}}, y)$$
where $\lambda_{\text{opt}} = 0.3$ and $\lambda_{\text{sar}} = 0.3$. During inference under severe cloud cover, if the optical cloud mask flag $\ge 80\%$, the pipeline automatically routes predictions through $\hat{y}_{\text{SAR}}$.

### 4.4 Region-Adaptive Phenology Alignment (RAM)
To eliminate classification and stress errors caused by staggered sowing across microclimates, temporal NDVI profiles are aligned using an adaptive Savitzky-Golay polynomial filter:
$$\text{NDVI}^*(t) = \sum_{i=-m}^{m} c_i \cdot \text{NDVI}(t + i)$$
From the continuous smoothed trajectory $\text{NDVI}^*(t)$, dynamic phenological markers are extracted:
1. **Start of Season (SOS):** Day of Year (DOY) where $\frac{d\text{NDVI}^*}{dt}$ reaches maximum positive acceleration (20% above seasonal baseline).
2. **Peak Vegetative Stage:** DOY where $\frac{d\text{NDVI}^*}{dt} = 0$ and $\text{NDVI}^* = \text{NDVI}_{\max}^*$.
3. **Length of Growing Period (LGP):** $\text{DOY}_{\text{senescence}} - \text{DOY}_{\text{SOS}}$.

---

## 5. Hydrological Engine & Mathematical Formulations

### 5.1 Phenology-Aware Multi-Index Stress Ensemble
Moisture stress is monitored dynamically across three growth stages:
* **Stage I:** Early Vegetative ($\text{SOS} \le t < \text{Peak} - 20\,\text{days}$)
* **Stage II:** Peak Flowering / Booting ($\text{Peak} - 20\,\text{days} \le t \le \text{Peak} + 15\,\text{days}$)
* **Stage III:** Late Ripening / Grain Filling ($\text{Peak} + 15\,\text{days} < t \le \text{EOS}$)

The ensemble synthesizes three indices:
1. **Vegetation Condition Index (VCI):**
   $$\text{VCI} = \frac{\text{NDVI} - \text{NDVI}_{\min}}{\text{NDVI}_{\max} - \text{NDVI}_{\min}} \times 100$$
2. **SAR Soil Moisture Index ($SMI_{\text{SAR}}$):**
   $$SMI_{\text{SAR}} = \frac{\sigma^\circ_{\text{VH}} - \sigma^\circ_{\text{VH},\min}}{\sigma^\circ_{\text{VH},\max} - \sigma^\circ_{\text{VH},\min}} \times 100$$
3. **Thermal Anomaly Index ($TAI_{\text{LST}}$):**
   $$TAI_{\text{LST}} = \frac{\text{LST}_{\text{observed}} - \mu_{\text{LST},30\text{d}}}{\sigma_{\text{LST},30\text{d}}}$$

Composite Moisture Stress Index:
$$\text{CMSI} = w_{\text{VCI}} \cdot (100 - \text{VCI}) + w_{\text{SMI}} \cdot (100 - SMI_{\text{SAR}}) + w_{\text{TAI}} \cdot \text{Clip}(TAI_{\text{LST}} \times 20, 0, 100)$$

| Stage | $w_{\text{VCI}}$ (Optical Canopy) | $w_{\text{SMI}}$ (Radar Root-Zone) | $w_{\text{TAI}}$ (Thermal Transpiration) |
| :--- | :--- | :--- | :--- |
| **Early Vegetative** | 0.20 | 0.60 | 0.20 |
| **Peak Flowering** | 0.35 | 0.35 | 0.30 |
| **Late Ripening** | 0.50 | 0.30 | 0.20 |

#### Stress Categorization:
* $\text{CMSI} < 30$: **No Stress** (Normal Hydrology)
* $30 \le \text{CMSI} < 50$: **Mild Moisture Deficit**
* $50 \le \text{CMSI} < 70$: **Moderate Stress** (Immediate Irrigation Required)
* $\text{CMSI} \ge 70$: **Severe Stress** (Severe Yield Loss Imminent)

### 5.2 8-Day Hargreaves-Samani & FAO-56 Water Deficit Engine

#### 1. Reference Evapotranspiration ($ET_o$):
Calculated using the Hargreaves-Samani equation, which requires only temperature and solar geometry:
$$ET_o = 0.0023 \times (T_{\text{avg}} + 17.8) \times (T_{\max} - T_{\min})^{0.5} \times \frac{R_a}{2.45}$$
where:
* $T_{\text{avg}} = \frac{T_{\max} + T_{\min}}{2}$ (in $^\circ\text{C}$)
* $R_a$ is extraterrestrial radiation ($\text{MJ}/\text{m}^2/\text{day}$):
  $$R_a = \frac{24 \times 60}{\pi} G_{sc} \cdot d_r \cdot \Big(\omega_s \sin(\phi)\sin(\delta) + \cos(\phi)\cos(\delta)\sin(\omega_s)\Big)$$
  with solar constant $G_{sc} = 0.0820\,\text{MJ}/\text{m}^2/\text{min}$, inverse relative distance Earth-Sun $d_r = 1 + 0.033\cos\left(\frac{2\pi}{365}J\right)$, solar declination $\delta = 0.409\sin\left(\frac{2\pi}{365}J - 1.39\right)$, and sunset hour angle $\omega_s = \arccos(-\tan(\phi)\tan(\delta))$.

#### 2. Actual Crop Evapotranspiration ($ET_c$):
$$ET_c = K_c(\text{stage}) \times ET_o$$
Crop coefficient $K_c$ values for target agro-climatic zones:

| Crop Type | $K_{c,\text{ini}}$ (Vegetative) | $K_{c,\text{mid}}$ (Flowering) | $K_{c,\text{end}}$ (Maturity) |
| :--- | :--- | :--- | :--- |
| **Paddy Rice** | 1.05 | 1.20 | 0.90 |
| **Cotton** | 0.35 | 1.15 | 0.65 |
| **Maize** | 0.30 | 1.20 | 0.35 |
| **Sugarcane** | 0.40 | 1.25 | 0.75 |
| **Pulses / Gram**| 0.40 | 1.05 | 0.30 |

#### 3. Actual Crop Evapotranspiration ($ET_a$):
$$ET_a = ET_o \times \left(\frac{\text{NDVI} - \text{NDVI}_{\text{soil}}}{\text{NDVI}_{\max} - \text{NDVI}_{\text{soil}}}\right)^{0.5}$$

#### 4. Effective Rainfall ($P_{\text{eff}}$):
Accounts for surface runoff and deep percolation under intense precipitation:
$$P_{\text{eff}} = \begin{cases} 0.8 \times P_{\text{total}} - 5, & \text{if } P_{\text{total}} > 10\,\text{mm/day} \\ 0, & \text{if } P_{\text{total}} \le 10\,\text{mm/day} \end{cases}$$

#### 5. Net 8-Day Volumetric Water Deficit:
$$\text{Deficit}_{8} = \max\left(0,\, \sum_{d=1}^{8} \Big(ET_c(d) - ET_a(d) - P_{\text{eff}}(d)\Big)\right)\quad[\text{mm}]$$

Conversion to volumetric requirement per canal command block of area $A_{\text{block}}$ (hectares):
$$V_{\text{water}} = \text{Deficit}_8 \times 10 \times A_{\text{block}}\quad[\text{m}^3]$$
*(Note: $1\,\text{mm} = 10\,\text{m}^3/\text{ha}$)*.

#### 6. Sluice Gate Discharge Release Recommendation:
For an irrigation operating window of $t_{\text{irr}} = 48\,\text{hours}$:
$$Q_{\text{sluice}} = \frac{V_{\text{water}}}{t_{\text{irr}} \times 3600 \times \eta_{\text{canal}}}\quad[\text{m}^3/\text{s}\text{ or cumecs}]$$
where $\eta_{\text{canal}} = 0.70$ is the standard canal conveyance efficiency factor.

---

## 6. Modular Codebase Architecture

The project codebase is partitioned into a high-performance Python/FastAPI backend and a modern React client application:

```
Grove/
├── .gitignore               # Standard Python, Node, ML checkpoints & Geospatial rasters
├── README.md                # Project README & quickstart
├── prd.md                   # Product Requirements Document (/to-spec format)
├── architecture.md          # Technical Architecture & System Specification
├── backend/                 # Python / PyTorch / FastAPI Service
│   ├── requirements.txt     # Pinned Python dependencies
│   ├── main.py              # FastAPI server & route orchestration
│   ├── gee_pipeline.py      # Earth Engine pipeline & raster exporter
│   ├── data_loader.py       # Memory-mapped raster loader & PyTorch datasets
│   ├── model.py             # Prithvi-EO ViT, SAR 2D CNN, MSF-Net, RF fallback
│   ├── stress.py            # Savitzky-Golay RAM tracker & stress ensemble
│   └── hydrology.py         # Hargreaves ET0, FAO-56 balance, 8-day deficit
├── frontend/                # React (TypeScript + Vite) Client Application
│   ├── package.json         # Node dependencies (React 18+, MapLibre/Leaflet, Recharts)
│   ├── vite.config.ts       # Vite bundler configuration & proxy settings
│   ├── src/
│   │   ├── App.tsx          # Root application layout & state provider
│   │   ├── components/
│   │   │   ├── MapViewer.tsx        # GPU-accelerated raster/vector GIS map viewer
│   │   │   ├── CanalAdvisory.tsx    # Sluice release tables, discharge gauges (Q = V / t)
│   │   │   ├── PhenologyChart.tsx   # Recharts dynamic Savitzky-Golay time-series
│   │   │   └── StressGauge.tsx      # Composite moisture stress breakdown cards
│   │   └── services/
│   │       └── api.ts               # Axios / Fetch client connecting to FastAPI
└── tests/
    ├── test_hydrology.py    # Unit tests for Hargreaves, Kc, and deficit equations
    ├── test_model.py        # Tensor shape, auxiliary loss, and fallback verification
    └── test_stress.py       # Savitzky-Golay curve fitting and stress weighting tests
```

### Module Interface Specifications

#### Module 1: `gee_pipeline.py`
```python
class GEEPipeline:
    def __init__(self, project_id: str, service_account: Optional[str] = None):
        """Authenticates with Earth Engine and initializes API session."""
        
    def export_composite_chip(
        self, 
        roi_geojson: dict, 
        start_date: str, 
        end_date: str,
        output_path: str
    ) -> str:
        """
        Runs cloud-masked S2, Refined Lee filtered S1, Landsat-8 LST, and ERA5 extraction.
        Exports multi-band 10m GeoTIFF composite chip.
        """
```

#### Module 2: `data_loader.py`
```python
class CropFeatureDataset(torch.utils.data.Dataset):
    def __init__(self, geotiff_path: str, patch_size: int = 11, temporal_steps: int = 3):
        """Loads raster bands using rasterio windowed reads and memory-mapping."""
        
    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, torch.Tensor, dict]:
        """
        Returns:
            optical_tensor: (T, 6, 224, 224)
            sar_patch:      (2, 11, 11)
            metadata:       Spatial coordinates, CRS, parcel ID
        """
```

#### Module 3: `model.py`
```python
class MSFNetCropClassifier(nn.Module):
    def __init__(self, num_classes: int = 6, pretrained: bool = True):
        """Asymmetric late-fusion model combining Prithvi ViT and SAR Conv2D."""
        
    def forward(
        self, 
        optical: torch.Tensor, 
        sar: torch.Tensor
    ) -> Tuple[torch.Tensor, torch.Tensor, torch.Tensor]:
        """Returns (logits_fused, logits_optical, logits_sar)."""

class RandomForestCropClassifier:
    def __init__(self, n_estimators: int = 100):
        """Scikit-Learn fallback model for zero-GPU environments."""
        
    def fit(self, X: np.ndarray, y: np.ndarray) -> None: ...
    def predict(self, X: np.ndarray) -> np.ndarray: ...
```

#### Module 4: `stress.py`
```python
class PhenologyStressEngine:
    def fit_savgol_phenology(self, ndvi_series: np.ndarray, window_length: int = 7) -> dict:
        """Extracts SOS, Peak, and LGP day-of-year markers."""
        
    def calculate_cmsi(
        self, 
        vci: np.ndarray, 
        smi: np.ndarray, 
        tai: np.ndarray, 
        stage: str
    ) -> np.ndarray:
        """Computes Composite Moisture Stress Index [0..100]."""
```

#### Module 5: `hydrology.py`
```python
class HydrologyBalanceEngine:
    def hargreaves_et0(
        self, 
        t_min: np.ndarray, 
        t_max: np.ndarray, 
        latitude: float, 
        doy: int
    ) -> np.ndarray:
        """Calculates Reference Evapotranspiration in mm/day."""
        
    def calculate_8day_sluice_advisories(
        self, 
        deficit_mm: np.ndarray, 
        area_ha: float, 
        efficiency: float = 0.70
    ) -> dict:
        """Outputs total volume in m^3 and recommended discharge in m^3/s."""
```

#### Module 6: Backend REST API (`backend/main.py`) & React Frontend (`frontend/`)

##### A. Backend REST API Endpoints (`FastAPI`):
* `GET /api/v1/health`: Cluster & GPU status probe.
* `GET /api/v1/crops/geojson`: Streams 10m vectorized crop classification parcel boundaries.
* `GET /api/v1/stress/tiles/{z}/{x}/{y}.png`: Dynamic XYZ map tile server rendering Stage-Wise Moisture Stress heatmaps.
* `GET /api/v1/canals/advisories`: Returns 8-day volumetric water deficit ($m^3/\text{ha}$) and sluice discharge metrics ($Q = V / t$) per canal distributary.
* `GET /api/v1/pixel/timeseries?lat={lat}&lon={lon}`: Delivers raw and Savitzky-Golay smoothed NDVI, $SMI_{\text{SAR}}$, and LST temporal profiles for pixel-level drill-down.

##### B. Frontend Application (`React + Vite + TypeScript`):
* **Technology Stack:** React 18/19, Vite, TypeScript, MapLibre GL / React-Leaflet, Recharts, TailwindCSS / Vanilla CSS, Lucide Icons.
* **Component Architecture:**
  1. **`MapViewer.tsx`**: Interactive dual-layer WebGL/Leaflet GIS map with toggleable 10m crop classification boundaries and stage moisture stress heatmaps. Supports click-to-inspect on any parcel.
  2. **`CanalAdvisory.tsx`**: Responsive data table and metric cards showing aggregated 8-day water deficit ($m^3/\text{ha}$), current crop stage, and recommended sluice discharge ($m^3/s$) with status indicators (Normal, Alert, Critical).
  3. **`PhenologyChart.tsx`**: Interactive Recharts time-series chart plotting temporal Savitzky-Golay smoothed NDVI curves, radar moisture index ($SMI_{\text{SAR}}$), and thermal anomalies ($TAI_{\text{LST}}$).
  4. **`ExportAdvisory.tsx`**: Official PDF and CSV report generator for irrigation engineers and field sluice operators.

---

## 7. Performance Benchmarks & Edge Scaling

* **Inference Latency:** < 120 seconds for an entire $10\,\text{km} \times 10\,\text{km}$ ($10,000\,\text{ha}$) canal command block on a standard 4-core CPU or consumer laptop GPU (e.g., RTX 3060 / 4060).
* **Memory Footprint:** Uses FP16 mixed precision (`torch.cuda.amp.autocast`) and windowed raster chunking ($512 \times 512$ pixel blocks), restricting peak RAM usage to $< 3.5\,\text{GB}$.
* **Data Transmission:** Raw Sentinel/Landsat satellite scenes are processed in the GEE cloud; only the compiled 10m 12-channel feature GeoTIFF (~45 MB per $100\,\text{km}^2$) is streamed to the local node.
* **Accuracy Metrics:**
  * Multi-crop overall classification accuracy: $\ge 88.5\%$ F1-score across 5 target crops.
  * Cloudy season radar standalone accuracy: $\ge 82.0\%$ F1-score (avoiding optical blackout failure).
  * Volumetric irrigation deficit concordance with in-situ soil moisture probes: $R^2 \ge 0.81$.
