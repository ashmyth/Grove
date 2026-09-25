# Technical Architecture & System Specification: Grove (GeoPrithvi-Agri)

> **Note:** This document is mirrored as [`architecture.md`](./architecture.md).

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
                      [STREAMLIT INTERACTIVE DASHBOARD]
        ├── 10m Spatial Crop Classification Boundary Layer (Leaflet / Folium)
        ├── Stage-Wise Moisture Stress Categorization (None, Mild, Moderate, Severe)
        ├── Canal Command Block Aggregated Sluice Release Advisories (Q = V / t)
        └── Dynamic Pixel-Level Phenological Curve Inspector (Plotly)
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
| **Frontend & UI** | Interactive Web Dashboard | **Streamlit >= 1.28.0**, **Streamlit-Folium >= 0.15.0** | Production dashboard with interactive raster tile layers, vector polygon overlays, and responsive parameter sliders. |
| **Data Visualization** | Scientific Plotting | **Plotly >= 5.17.0** | Interactive, GPU-accelerated phenology curves, stage-wise water deficit profiles, and sluice discharge plots. |

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
* **Refined Lee Speckle Filtering:** Applied using a $7 \times 7$ moving directional adaptive window:
  $$\hat{I} = \bar{I} + W \cdot (I - \bar{I})$$
  where the weighting factor $W$ is:
  $$W = \frac{\text{Var}(I) - \bar{I}^2 \cdot \sigma_v^2}{\text{Var}(I) \cdot (1 + \sigma_v^2)}$$
* **Dual-Polarization Polarimetric Proxies:**
  * **Volume Scattering Proxy ($m_v$):**
    $$m_v = \frac{4 \cdot \sigma^\circ_{\text{VH}}}{\sigma^\circ_{\text{VV}} + \sigma^\circ_{\text{VH}}}$$
  * **Surface Scattering Proxy ($m_s$):**
    $$m_s = \frac{\sigma^\circ_{\text{VV}} - \sigma^\circ_{\text{VH}}}{\sigma^\circ_{\text{VV}} + \sigma^\circ_{\text{VH}}}$$

### 3.3 Thermal Infrared (Landsat-8 TIRS Band 10)
* **Resolution:** $100\text{m}$ native resampled to $10\text{m}$ via bicubic spline interpolation matched to the Sentinel grid.
* **Land Surface Temperature (LST) Calculation:**
  $$T_B = \frac{K_2}{\ln\left(\frac{K_1}{L_\lambda} + 1\right)}$$
  $$\text{LST} = \frac{T_B}{1 + \left(\lambda \cdot \frac{T_B}{\rho}\right) \cdot \ln(\epsilon)}$$

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
          features = self.backbone(x).last_hidden_state
          pooled = torch.mean(features, dim=1)
          return F.relu(self.proj(pooled))
  ```

### 4.2 SAR Structural Branch (2D CNN Spatial Patch Encoder)
Processes $11 \times 11$ pixel spatial patches of Sentinel-1 dual-polarization ($\text{VV}, \text{VH}$) data centered on the target parcel to extract micro-texture, roughness, and dielectric gradients.

### 4.3 Asymmetric Multimodal Late-Fusion Network (`MSF-Net`)
Fuses the 256-dimensional optical ViT vector and the 256-dimensional radar CNN vector via element-wise addition:
$$f_{\text{fused}} = f_{\text{optical}} \oplus f_{\text{SAR}} \in \mathbb{R}^{256}$$

#### Auxiliary Loss Regularization:
$$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{CE}}(\hat{y}_{\text{fused}}, y) + \lambda_{\text{opt}}\mathcal{L}_{\text{CE}}(\hat{y}_{\text{optical}}, y) + \lambda_{\text{sar}}\mathcal{L}_{\text{CE}}(\hat{y}_{\text{SAR}}, y)$$
where $\lambda_{\text{opt}} = 0.3$ and $\lambda_{\text{sar}} = 0.3$. During inference under severe cloud cover, if the optical cloud mask flag $\ge 80\%$, the pipeline automatically routes predictions through $\hat{y}_{\text{SAR}}$.

### 4.4 Region-Adaptive Phenology Alignment (RAM)
Temporal NDVI profiles are aligned using an adaptive Savitzky-Golay polynomial filter:
$$\text{NDVI}^*(t) = \sum_{i=-m}^{m} c_i \cdot \text{NDVI}(t + i)$$
Extracts dynamic phenological markers: Start of Season (SOS), Peak Vegetative Stage, and Length of Growing Period (LGP).

---

## 5. Hydrological Engine & Mathematical Formulations

### 5.1 Phenology-Aware Multi-Index Stress Ensemble
Monitors moisture stress dynamically across three growth stages:
* **Stage I:** Early Vegetative
* **Stage II:** Peak Flowering / Booting
* **Stage III:** Late Ripening / Grain Filling

Synthesizes three indices:
1. **Vegetation Condition Index (VCI):**
   $$\text{VCI} = \frac{\text{NDVI} - \text{NDVI}_{\min}}{\text{NDVI}_{\max} - \text{NDVI}_{\min}} \times 100$$
2. **SAR Soil Moisture Index ($SMI_{\text{SAR}}$):**
   $$SMI_{\text{SAR}} = \frac{\sigma^\circ_{\text{VH}} - \sigma^\circ_{\text{VH},\min}}{\sigma^\circ_{\text{VH},\max} - \sigma^\circ_{\text{VH},\min}} \times 100$$
3. **Thermal Anomaly Index ($TAI_{\text{LST}}$):**
   $$TAI_{\text{LST}} = \frac{\text{LST}_{\text{observed}} - \mu_{\text{LST},30\text{d}}}{\sigma_{\text{LST},30\text{d}}}$$

Composite Moisture Stress Index:
$$\text{CMSI} = w_{\text{VCI}} \cdot (100 - \text{VCI}) + w_{\text{SMI}} \cdot (100 - SMI_{\text{SAR}}) + w_{\text{TAI}} \cdot \text{Clip}(TAI_{\text{LST}} \times 20, 0, 100)$$

### 5.2 8-Day Hargreaves-Samani & FAO-56 Water Deficit Engine

1. **Reference Evapotranspiration ($ET_o$):**
   $$ET_o = 0.0023 \times (T_{\text{avg}} + 17.8) \times (T_{\max} - T_{\min})^{0.5} \times \frac{R_a}{2.45}$$
2. **Actual Crop Evapotranspiration Demand ($ET_c$):**
   $$ET_c = K_c(\text{stage}) \times ET_o$$
3. **Actual Crop Evapotranspiration ($ET_a$):**
   $$ET_a = ET_o \times \left(\frac{\text{NDVI} - \text{NDVI}_{\text{soil}}}{\text{NDVI}_{\max} - \text{NDVI}_{\text{soil}}}\right)^{0.5}$$
4. **Effective Rainfall ($P_{\text{eff}}$):**
   $$P_{\text{eff}} = \begin{cases} 0.8 \times P_{\text{total}} - 5, & \text{if } P_{\text{total}} > 10\,\text{mm/day} \\ 0, & \text{if } P_{\text{total}} \le 10\,\text{mm/day} \end{cases}$$
5. **Net 8-Day Volumetric Water Deficit:**
   $$\text{Deficit}_{8} = \max\left(0,\, \sum_{d=1}^{8} \Big(ET_c(d) - ET_a(d) - P_{\text{eff}}(d)\Big)\right)\quad[\text{mm}]$$
   $$V_{\text{water}} = \text{Deficit}_8 \times 10 \times A_{\text{block}}\quad[\text{m}^3]$$
6. **Sluice Gate Discharge Release Recommendation:**
   $$Q_{\text{sluice}} = \frac{V_{\text{water}}}{t_{\text{irr}} \times 3600 \times \eta_{\text{canal}}}\quad[\text{m}^3/\text{s}]$$

---

## 6. Modular Codebase Architecture

```
Grove/
├── .gitignore               # Standard Python, ML checkpoints & Geospatial rasters
├── README.md                # Project README & quickstart
├── prd.md                   # Product Requirements Document (/to-spec format)
├── architecture.md          # Technical Architecture & System Specification
├── archicture.md            # Exact mirror of architecture.md
├── requirements.txt         # Pinned production dependencies
├── data/                    # Local sample GeoTIFFs, boundary GeoJSONs, shapefiles
├── src/
│   ├── __init__.py
│   ├── gee_pipeline.py      # Module 1: Earth Engine pipeline & raster exporter
│   ├── data_loader.py       # Module 2: Memory-mapped raster loader & PyTorch datasets
│   ├── model.py             # Module 3: Prithvi-EO ViT, SAR 2D CNN, MSF-Net, RF fallback
│   ├── stress.py            # Module 4: Savitzky-Golay RAM tracker & stress ensemble
│   ├── hydrology.py         # Module 5: Hargreaves ET0, FAO-56 balance, 8-day deficit
│   └── app.py               # Module 6: Streamlit dashboard & Leaflet spatial engine
└── tests/
    ├── test_hydrology.py    # Unit tests for Hargreaves, Kc, and deficit equations
    ├── test_model.py        # Tensor shape, auxiliary loss, and fallback verification
    └── test_stress.py       # Savitzky-Golay curve fitting and stress weighting tests
```

---

## 7. Performance Benchmarks & Edge Scaling

* **Inference Latency:** < 120 seconds for an entire $10\,\text{km} \times 10\,\text{km}$ ($10,000\,\text{ha}$) canal command block on a standard 4-core CPU or consumer laptop GPU (e.g., RTX 3060 / 4060).
* **Memory Footprint:** Uses FP16 mixed precision (`torch.cuda.amp.autocast`) and windowed raster chunking ($512 \times 512$ pixel blocks), restricting peak RAM usage to $< 3.5\,\text{GB}$.
* **Data Transmission:** Raw Sentinel/Landsat satellite scenes are processed in the GEE cloud; only the compiled 10m 12-channel feature GeoTIFF (~45 MB per $100\,\text{km}^2$) is streamed to the local node.
* **Accuracy Metrics:**
  * Multi-crop overall classification accuracy: $\ge 88.5\%$ F1-score across 5 target crops.
  * Cloudy season radar standalone accuracy: $\ge 82.0\%$ F1-score (avoiding optical blackout failure).
  * Volumetric irrigation deficit concordance with in-situ soil moisture probes: $R^2 \ge 0.81$.
