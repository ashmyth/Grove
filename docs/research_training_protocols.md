# GeoPrithvi-Agri — Empirical Research & Training Protocols

This document enshrines the research-backed training methodologies, architectural philosophies, and empirical findings governing the GeoPrithvi-Agri AI models (MSF-Net, Prithvi-EO ViT, and Multi-Sensor Classifiers).

---

## 1. Preprocessing Philosophy: 7-Day Linear Resampling
* **Empirical Finding:** Monthly (30-day) aggregation smooths out critical, rapid phenological transition milestones (such as short flowering or heading windows), leading to significant drops in crop identification accuracy. Whittaker-Eilers (WE) filtering oversmooths and destroys subtle within-season spectral variations. Raw, un-composited series introduce irregular date gaps that destabilize sequential neural encoders.
* **Adopted Protocol:** **Fixed 7-Day Linear Resampling**. Consistently achieves ~95.2% Overall Accuracy by establishing a standardized, dense temporal matrix without losing rapid vegetative growth signals.

---

## 2. Fusion Architecture: Asymmetric Late-Fusion (MSF-Net)
* **Empirical Finding:** In smallholder, fragmented agricultural landscapes with limited field labels, heavy 3D Spatiotemporal Vision Transformers (TSViT) or ConvGRU dual-streams (TWINNS) overfit, show high inter-fold variance (>8%), and require 4.7× to 6.1× longer to train and 13× to 14× longer to evaluate.
* **Adopted Protocol:** **Asymmetric Dual-Branch Late Fusion (MSF-Net)**.
  - Spatial SAR patch encoder: 2D CNN (capturing surface roughness and canopy structure).
  - Multi-temporal optical encoder: 1D TempCNN (capturing spectral reflectance curves).
  - Fusion mechanism: Element-wise vector addition ($\mathbf{f}_{\text{fused}} = \mathbf{f}_{\text{opt}} \oplus \mathbf{f}_{\text{sar}}$).
  - Benefits: Acts as an implicit regularizer, cuts map salt-and-pepper noise by >50%, and executes over 10× faster.

---

## 3. Loss Regularization: Multi-Task Auxiliary Supervision
* **Empirical Finding:** In overcast monsoon (Kharif) seasons, persistent optical cloud cover degrades the optical branch representations, polluting a single fused output head.
* **Adopted Protocol:** **Branch-Specific Auxiliary Supervision** with loss weighting $\lambda_1 = \lambda_2 = 0.3$:
  $$\mathcal{L}_{\text{total}} = \mathcal{L}_{\text{fusion}} + 0.3 \cdot \mathcal{L}_{\text{aux\_optical}} + 0.3 \cdot \mathcal{L}_{\text{aux\_sar}}$$
* **Impact:** Delivers up to +30 percentage points in F1-score on spectrally ambiguous crops (e.g., cotton or shrubby vegetation) and forces the SAR branch to remain an effective standalone classifier during complete optical blackouts.

---

## 4. Ground-Truth Quality & Sample Thresholding
* **Empirical Finding:** Including underrepresented crop classes with fewer than 1,500 samples degrades overall model accuracy down to ~77–80% because decision boundaries fail to generalize.
* **Adopted Protocols:**
  1. **Multi-Year Rotation Filtering ("Trusted Pixels"):** Verify parcel labels against historical crop rotations to eliminate mislabeled field survey errors.
  2. **1,500-Sample Filtering Threshold:** Prune or merge rare classes with <1,500 samples, lifting overall classification accuracy from 78.3% to >91.6%.

---

## 5. Class Imbalance Strategy: Balanced Subset Undersampling
* **Empirical Finding:** Aggressive inverse-frequency loss weighting causes high training gradient variance and sharply inflates false-positive rates on dominant background classes.
* **Adopted Protocol:** **Balanced Subset Undersampling (R3 Strategy)**. Uniformly downsample majority classes to match minority class proportions during initial training epochs (~25 epochs), then restore representative distribution for final calibration.

---

## 6. Cross-Regional Generalization: Region-Aware Environmental Embeddings (RAM)
* **Empirical Finding:** Topography (elevation, slope) and microclimate gradients trigger 3- to 4-week phenological shifts ($\Delta t$) between different agroclimatic zones. Fixed-calendar models experience severe cross-regional performance decay (15.6% mIoU decay).
* **Adopted Protocol:** **Region-Aware Module (RAM)**.
  - Encodes static terrain (SRTM 30m DEM elevation and slope) via a 2D ResNet-18.
  - Encodes 1D monthly temperature and precipitation trends (ECMWF ERA5-Land).
  - Emits a Regional Embedding vector ($\mathbf{RE}$) that dynamically predicts temporal shift offsets ($\Delta t$) and adjusts temporal attention windows, cutting cross-regional transfer decay from 15.6% down to 8.7%–9.5%.

---

## 7. Transfer Learning & Sample Size Thresholds
* **Supervised Plateau:** Supervised classification accuracy plateaus once labeled samples reach **~3,000 samples per crop class** per satellite scene footprint.
* **Unsupervised Domain Adaptation (UDA):** When target-domain labels are zero, Domain-Adversarial Neural Networks (DANN) align feature distributions for homogeneous crops.
* **Agroclimatic Domain Shift:** Under severe agroclimatic shifts, fine-tuning foundation backbones (IBM-NASA Prithvi-EO 100M) via **LoRA (Low-Rank Adaptation)** on 1,000–3,000 local labels provides maximum stability.

---

## 8. Sensor Complementarity: Tri-Modal Optical + SAR + Thermal Fusion
* **Empirical Finding:** Optical greenness (NDVI, EVI) and SAR backscatter ($\sigma^0_{\text{VV}}$, $\sigma^0_{\text{VH}}$) capture canopy color and structural biomass, but miss root-zone transpiration cooling.
* **Adopted Protocol:** **Tri-Modal Fusion (Optical + SAR + Landsat-8 TIRS LST)**. Integrating Land Surface Temperature anomalies resolves spectrally overlapping crops through differential evaporative cooling signatures, elevating peak multi-sensor classification accuracy to 92.08%.

---

## Protocol Implementation Matrix

| Phase | Selected Method | Target Metric / Benchmark |
| :--- | :--- | :--- |
| **Preprocessing** | 7-Day Linear Resampling | 95.2% Overall Accuracy |
| **Label Quality** | Trusted Pixels + $\ge 1,500$ Samples/Class | $>91.6\%$ Accuracy Threshold |
| **Architecture** | Asymmetric Late-Fusion (MSF-Net) | 10× Evaluation Speedup vs 3D ViT |
| **Loss Function** | Multi-Task Heads ($\lambda = 0.3$) | +30pt F1 on Ambiguous Crops |
| **Balancing** | Subset Undersampling (R3 Strategy) | High Minority Precision |
| **Phenology** | Region-Aware Module (RAM: SRTM + ERA5) | Decay Rate Reduced from 15.6% to 8.7% |
| **Modalities** | Optical MSI + C-Band SAR + Thermal LST | 92.08% Tri-Modal Classification |
