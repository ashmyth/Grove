# Product Requirements Document (PRD) — Grove (GeoPrithvi-Agri)

**Project Title:** AI-Driven Automated Crop Mapping, Stage-Wise Moisture Stress Detection, and 8-Day Canal Command Irrigation Advisory System  
**Product Codename:** Grove / GeoPrithvi-Agri  
**Document Status:** Ready for Engineering Review  
**Specification Standard:** `/to-spec` (Synthesis from Technical Architecture & Domain Specs)

---

## Problem Statement

Traditional agricultural monitoring and canal irrigation scheduling in smallholder farming environments face severe operational and hydrological bottlenecks:

1. **Persistent Monsoon Cloud Contamination:** During the Indian *Kharif* season (June–October), cloud cover severely degrades optical satellite sensors (Sentinel-2, Landsat-8/9), producing blind spots lasting weeks at critical crop phenological stages.
2. **Phenological Phase Shifts:** Variations in terrain elevation, local microclimates, and irregular sowing dates trigger significant growth stage shifts across adjacent blocks, rendering rigid, calendar-driven canal release schedules inaccurate and wasteful.
3. **Spectral Mixing in Fragmented Smallholder Fields:** Farmlands with plot sizes under 0.5–2 hectares produce severe mixed-pixel artifacts at 30m resolution, confusing crop boundaries and misclassifying spectrally similar crops (e.g., cotton vs. maize, or paddy rice vs. semi-aquatic weed clusters).
4. **Disjointed Irrigation Allocation:** Canal irrigation authorities manage sluice gates without real-time, spatialized field-scale crop water deficit data, leading to severe upstream water wastage and acute tail-end water starvation.
5. **Compute & Infrastructure Constraints:** Rural agricultural departments and field engineers lack access to multi-GPU clusters to run heavy Earth Observation transformer pipelines on terabytes of raw satellite imagery.

---

## Solution

**Grove (GeoPrithvi-Agri)** is an integrated geospatial AI and satellite hydrology platform that unifies all-weather radar, multispectral optical data, thermal sensing, and meteorological reanalysis into an automated crop mapping and irrigation advisory pipeline:

1. **All-Weather Multi-Source Sensor Fusion:** Fuses Sentinel-1 Synthetic Aperture Radar (SAR C-Band GRD with Refined Lee speckle filtering and polarimetric decomposition), Sentinel-2 MSI multispectral reflectance, Landsat-8 TIRS thermal band, and ERA5-Land reanalysis grids at 10m native/resampled resolution.
2. **Lightweight Geospatial Foundation Model:** Employs NASA/IBM's `Prithvi-EO-1.0-100M` ViT backbone as a frozen spatial-spectral feature extractor paired with an asymmetric 2D CNN radar branch (`MSF-Net` late-fusion) and a zero-GPU Scikit-Learn Random Forest fallback.
3. **Region-Adaptive Phenology Alignment (RAM):** Implements dynamic Savitzky-Golay filtering on temporal vegetation signals to derive Start of Season (SOS), Peak Vegetative, and Length of Growing Period (LGP), preventing false stress alarms from staggered sowing.
4. **Hydrological Water Deficit Engine:** Combines the Hargreaves-Samani $ET_o$ model with FAO-56 stage-specific crop coefficients ($K_c$) and effective rainfall calculations to generate actionable 8-day volumetric water deficit maps ($m^3/\text{ha}$ and $mm$ depth).
5. **Interactive Web Application (React Frontend):** Delivers a responsive, component-driven React web application (TypeScript + Vite) paired with a high-performance FastAPI backend, featuring interactive WebGL/Leaflet geospatial layers, canal command block aggregations, sluice gate discharge recommendations ($Q = V / t$), and parcel-level time-series inspectors.

---

## User Stories

### Persona 1: Canal Command Water Resources Engineer / Sluice Gate Operator
1. As a canal command engineer, I want to view an 8-day aggregated volumetric water deficit ($m^3/\text{ha}$) across each distributary and branch canal block, so that I can schedule sluice gate releases based on actual plant water stress rather than static timetables.
2. As a canal command engineer, I want the system to compute the required discharge rate ($m^3/s$ or cusecs) per sluice gate over an 8-day window, so that upstream and tail-end farmers receive equitable irrigation volumes.
3. As a canal command engineer, I want to filter water deficit alerts by canal reach (head, middle, tail-end), so that I can identify localized droughts and prevent tail-end crop failure.
4. As a canal command engineer, I want to export irrigation release schedules to CSV and PDF formats, so that field operators can execute manual sluice adjustments with official documentation.

### Persona 2: Smallholder Farmer / Farmer Producer Organization (FPO) Leader
5. As a smallholder farmer, I want to inspect my field parcel at 10m resolution, so that I can verify whether my plot is classified with the correct crop type.
6. As a smallholder farmer, I want to receive early stage-wise moisture stress warnings (Mild, Moderate, Severe), so that I can irrigate or apply mulching before irreversible wilting occurs.
7. As a smallholder farmer, I want stress assessments that account for my actual sowing date, so that normal early vegetative stages are not falsely flagged as drought stress.
8. As an FPO leader, I want to visualize aggregated crop acreage and moisture stress indices across all members in a village, so that I can bulk-order irrigation equipment or water tankers during dry spells.

### Persona 3: Agricultural Extension Officer / District Agronomist
9. As an agricultural extension officer, I want automated crop classification maps generated at 10m resolution, so that I can track seasonal cropping patterns without labor-intensive manual field surveys.
10. As an agricultural extension officer, I want to distinguish between high-water-demand crops (e.g., paddy rice, sugarcane) and low-water crops (e.g., millets, pulses), so that I can recommend crop diversification in water-stressed blocks.
11. As an agricultural extension officer, I want to examine temporal Land Surface Temperature (LST) anomaly curves alongside NDVI trajectories, so that I can identify transpiration failure caused by root-zone salinity or waterlogging.
12. As an agricultural extension officer, I want to receive automated advisories in regional languages on the dashboard, so that I can disseminate practical irrigation instructions to local farm groups.

### Persona 4: Crop Insurance Auditor (PMFBY Officer)
13. As a crop insurance auditor, I want continuous SAR-derived Soil Moisture Index ($SMI_{\text{SAR}}$) logs during monsoon months, so that I can audit localized flood or drought claims even when optical satellite imagery was fully cloud-covered.
14. As a crop insurance auditor, I want historic multi-year baseline comparisons of Vegetation Condition Index (VCI) and crop yield proxies, so that I can verify whether an insured parcel suffered an authentic yield shortfall.
15. As a crop insurance auditor, I want tamper-proof, timestamped geospatial reports for audited coordinates, so that insurance claim disbursements comply with national agricultural mission guidelines.

### Persona 5: Geospatial Data & ML Engineer
16. As an ML engineer, I want raw multispectral and radar scenes processed directly on Google Earth Engine (GEE), so that massive raw satellite data transfers are eliminated and only compressed 10m feature GeoTIFFs are ingested locally.
17. As an ML engineer, I want a frozen `Prithvi-EO-1.0-100M` backbone with a lightweight MLP head, so that inference runs in under 2 minutes on consumer hardware or free Google Colab tiers.
18. As an ML engineer, I want a dual-branch late-fusion architecture (`MSF-Net`) with branch-specific auxiliary loss heads, so that the model automatically falls back to SAR predictions when optical bands are obscured.
19. As an ML engineer, I want a Scikit-Learn Random Forest fallback module, so that inference executes successfully on CPU-only machines lacking PyTorch GPU acceleration.
20. As a data engineer, I want memory-mapped raster loading (`rasterio` windowed reads and `numpy.memmap`), so that 100-megapixel regional GeoTIFFs can be processed without Out-Of-Memory (OOM) crashes.
21. As a data engineer, I want automated polarimetric decomposition ($m_v$ volume scattering, $m_s$ surface scattering) and Refined Lee filtering on Sentinel-1 GRD scenes, so that radar speckle is removed without blurring field boundaries.

### Persona 6: Hydrologist & Irrigation Modeler
22. As a hydrologist, I want Reference Evapotranspiration ($ET_o$) calculated via the temperature-and-radiation-based Hargreaves-Samani formulation, so that calculation remains accurate even in data-sparse rural catchments without full weather stations.
23. As a hydrologist, I want stage-dependent crop coefficients ($K_{c,\text{ini}}, K_{c,\text{mid}}, K_{c,\text{end}}$) dynamically linked to the Savitzky-Golay phenology tracker, so that crop water demand ($ET_c$) adjusts precisely with vegetative growth.
24. As a hydrologist, I want effective rainfall ($P_{\text{eff}}$) computed using empirical agricultural runoff factors ($0.8 \times P_{\text{total}}$), so that non-infiltrating monsoon storm bursts do not skew soil moisture balances.
25. As a system administrator, I want modular architecture with decoupled Python backend services and a dedicated React frontend application, so that UI components and backend AI/hydrology engines can scale and deploy independently.

---

## Implementation Decisions

### 1. Modules Built & Architectural Boundaries

The platform is strictly partitioned into a high-performance Python/PyTorch backend and a modern React frontend:

```
Grove Codebase Architecture
├── backend/
│   ├── api.py             # FastAPI REST endpoints serving GeoJSON, rasters & advisories
│   ├── gee_pipeline.py    # GEE cloud authentication, cloud-masking, SAR speckle filter, raster export
│   ├── data_loader.py     # Local/cloud raster ingestion, memory-mapped slicing, PyTorch Dataset wrappers
│   ├── model.py           # Prithvi-EO-100M ViT backbone, SAR 2D CNN branch, MSF-Net late fusion, RF fallback
│   ├── stress.py          # Savitzky-Golay RAM phenology tracker, multi-index stress ensemble (VCI, SMI, LST)
│   └── hydrology.py       # Hargreaves-Samani ET0, FAO-56 Kc, Peff, 8-day volumetric water deficit engine
└── frontend/              # Modern React + TypeScript + Vite web application
    ├── src/components/    # Interactive map, canal block tables, time-series charts
    └── src/services/      # REST API client connecting to FastAPI backend
```

### 2. Interfaces & API Contracts

#### A. Data Loader Interface (`data_loader.py`):
```python
def load_feature_cube(
    geotiff_path: str, 
    window: Optional[Tuple[int, int, int, int]] = None
) -> Tuple[np.ndarray, Dict[str, Any]]:
    """
    Returns:
        feature_cube: np.ndarray of shape (C, H, W) where C=12 (Optical 6, Radar 2, Thermal 1, Meteo 3)
        metadata: Dict containing CRS, affine transform, nodata values, bounds
    """
```

#### B. Model Inference Interface (`model.py`):
```python
class MultimodalCropClassifier(nn.Module):
    def forward(
        self, 
        optical_seq: torch.Tensor,   # Shape: (B, T, 6, H, W)
        sar_patches: torch.Tensor    # Shape: (B, 2, 11, 11)
    ) -> Dict[str, torch.Tensor]:
        """
        Returns:
            {
                "logits_fused": Tensor(B, num_classes),
                "logits_optical": Tensor(B, num_classes),
                "logits_sar": Tensor(B, num_classes)
            }
        """
```

#### C. Stress Engine Interface (`stress.py`):
```python
class PhenologyStressEngine:
    def compute_phenology_markers(
        self, 
        ndvi_timeseries: np.ndarray, 
        doy_vector: np.ndarray
    ) -> Dict[str, int]:
        """Extracts SOS, Peak, and LGP day-of-year markers."""
        
    def evaluate_stress_ensemble(
        self, 
        vci: np.ndarray, 
        smi: np.ndarray, 
        lst_anomaly: np.ndarray, 
        stage: str
    ) -> Tuple[np.ndarray, np.ndarray]:
        """Returns (composite_stress_score [0..100], stress_category_enum)."""
```

#### D. Hydrological Deficit Interface (`hydrology.py`):
```python
class HydrologyEngine:
    def calculate_et0_hargreaves(
        self, 
        t_min: np.ndarray, 
        t_max: np.ndarray, 
        ra: np.ndarray
    ) -> np.ndarray:
        """Computes daily Reference Evapotranspiration in mm/day."""
        
    def compute_8day_water_deficit(
        self, 
        et0_8day: np.ndarray, 
        kc_stage: np.ndarray, 
        actual_et: np.ndarray, 
        p_eff_8day: np.ndarray
    ) -> Dict[str, np.ndarray]:
        """Returns deficit in mm depth and volumetric requirement in m^3/ha."""
```

### 3. Developer Technical Clarifications
* **Dual Execution Modes:** The ML engine must initialize with an automated runtime probe. If CUDA or PyTorch geometric/HuggingFace dependencies are missing, the system silently defaults to `RandomForestCropClassifier` without user-facing disruption.
* **Coordinate Reference System (CRS) Policy:** All exported raster products are standardized to `EPSG:4326` (WGS84) for GEE processing and reprojected to the local UTM zone (e.g., `EPSG:32643` / `EPSG:32644` for Central/Peninsular India) during spatial area ($m^3/\text{ha}$) calculations to preserve metric accuracy.
* **No Cloud-Storage Mandate:** Intermediate satellite scenes do not require permanent S3/GCS buckets; the pipeline supports local temporary caching and direct GeoTIFF downloading via GEE Python API credentials.

---

## Testing Decisions

### Seams for Machine Verification
1. **Hydrological Equation Invariance Seam:** Direct unit test assertions verifying Hargreaves $ET_o$ and FAO-56 crop demand against standard benchmark FAO-56 tables (e.g., verifying that $ET_o$ with $T_{\text{min}}=18^\circ\text{C}, T_{\text{max}}=32^\circ\text{C}, R_a=15.2\,\text{MJ/m}^2/\text{day}$ matches published hydrological baselines within 1% error tolerance).
2. **Radar Branch Fallback Seam:** Unit tests feeding empty/NaN optical tensors to `MultimodalCropClassifier` to confirm the auxiliary radar branch produces valid, non-zero crop probability distributions without runtime exception.
3. **Savitzky-Golay Curve Smoothing Seam:** Synthetic noisy NDVI curve tests ensuring dynamic SOS (Start of Season) detection accurately identifies known injection peaks within a $\pm 3$-day window.
4. **Raster Shape & Dimension Seam:** PyTorch dataset loader tests ensuring multi-channel GeoTIFF tiles always conform to expected tensor dimensions `(B, C, H, W)` and properly normalize reflectance values into the $[0, 1]$ interval.
5. **React Frontend & REST API Integration Seam:** Headless integration and component test validation checking that default GeoJSON boundaries and mock canal blocks render without runtime error, and that API responses conform to typed TypeScript interfaces.

---

## Out of Scope

* **Autonomous Sluice Gate Actuation Hardware:** Grove outputs volumetric recommendations and discharge metrics; physical SCADA/IoT motor control is out of scope for this release.
* **High-Resolution Drone (UAV) Ingestion:** The current architecture is optimized for 10m–30m satellite data (Sentinel/Landsat); sub-meter drone flight orthomosaics are not supported.
* **Deep Groundwater Aquifer Numerical Modeling:** The system models root-zone soil moisture ($0\text{--}50\,\text{cm}$) and surface hydrology; deep unconfined aquifer MODFLOW simulations are excluded.
* **Multi-User Role-Based Access Control (RBAC) & Payment Gateways:** Grove is an open-source technical prototype and decision support system; commercial subscription billing is excluded.

---

## Further Notes

* **Alignment with Digital Agriculture Mission:** Standardized GeoTIFF outputs and crop classification geo-JSONs directly comply with the Government of India's AgriStack standard formats.
* **National Policy Linkage:** Volumetric water balance calculations directly support the micro-irrigation metrics mandated by *Pradhan Mantri Krishi Sinchayee Yojana (PMKSY)*.
* **License & Open Source Integrity:** Codebase is configured under the MIT License; all satellite sources utilized are free and open-access public data assets (Copernicus ESA, USGS NASA, ECMWF ERA5).
