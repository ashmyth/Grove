# Grove (GeoPrithvi-Agri)

**AI-Driven Automated Crop Mapping, Stage-Wise Moisture Stress Detection, and 8-Day Canal Command Irrigation Advisory System**

---

## 📌 Project Overview

**Grove (GeoPrithvi-Agri)** fuses multi-source satellite Earth Observation (EO) data—Synthetic Aperture Radar (Sentinel-1), multispectral optical imagery (Sentinel-2 / Landsat HLS), thermal infrared (Landsat-8 TIRS), and gridded meteorology (ERA5-Land)—with state-of-the-art geospatial foundation models (`Prithvi-EO-1.0-100M`) and satellite hydrology engines (Hargreaves-Samani & FAO-56).

It delivers automated 10m crop parcel boundary mapping, all-weather moisture stress tracking across phenological stages, and 8-day volumetric water deficit ($m^3/\text{ha}$) advisories for canal command sluice operations.

---

## 📚 Core Documentation

- 📋 **[Product Requirements Document (PRD)](./prd.md):** Complete specifications following `/to-spec` with extensive user stories, implementation decisions, and testing seams.
- 🏗️ **[Technical Architecture & System Specification](./architecture.md):** In-depth engineering design covering multi-modal neural architectures, GEE cloud offloading, SAR polarimetric processing, hydrological formulations, and React GIS dashboard architecture.
- 🗺️ **[Knowledge Graph Report](./graphify-out/GRAPH_REPORT.md):** Architectural relationship map, God Nodes, cross-cutting dependencies, and community clusters generated via [Graphify](https://github.com/Graphify-Labs/graphify). Interactive map available at [`graphify-out/graph.html`](./graphify-out/graph.html).

---

## 🛠️ Technology Stack

- **Geospatial & Cloud EO:** Google Earth Engine (GEE), Rasterio, GeoPandas, GDAL
- **Deep Learning & Foundation Models:** PyTorch, HuggingFace (`ibm-nasa-geospatial/Prithvi-100M`), TorchVision
- **Classical ML & Signal Processing:** Scikit-Learn (Random Forest Fallback), SciPy (Savitzky-Golay filtering)
- **Hydrology Engine:** Hargreaves-Samani $ET_o$, FAO-56 stage-wise $K_c$ water balance
- **Backend API:** FastAPI (Async REST endpoints, GeoJSON/raster streaming, Pydantic)
- **User Interface (Frontend):** React (TypeScript, Vite, MapLibre GL / Leaflet-React, Recharts, TailwindCSS)

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.