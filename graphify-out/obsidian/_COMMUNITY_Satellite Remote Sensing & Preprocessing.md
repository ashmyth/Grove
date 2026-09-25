---
type: community
cohesion: 0.25
members: 8
---

# Satellite Remote Sensing & Preprocessing

**Cohesion:** 0.25 - loosely connected
**Members:** 8 nodes

## Members
- [[Composite Moisture Stress Index (CMSI)]] - document - architecture.md
- [[PMFBY Crop Insurance Auditor]] - document - prd.md
- [[Region-Adaptive Phenology Alignment (RAM)]] - document - architecture.md
- [[SAR Soil Moisture Index (SMI_SAR)]] - document - architecture.md
- [[Savitzky-Golay Polynomial Smoother]] - document - architecture.md
- [[Split-Window LST Inversion]] - document - architecture.md
- [[Thermal Anomaly Index (TAI_LST)]] - document - architecture.md
- [[Vegetation Condition Index (VCI)]] - document - architecture.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Satellite_Remote_Sensing__Preprocessing
SORT file.name ASC
```

## Connections to other communities
- 3 edges to [[_COMMUNITY_Satellite Remote Sensing & Preprocessing_2]]
- 1 edge to [[_COMMUNITY_Hydrological Deficit & Sluice Scheduling]]
- 1 edge to [[_COMMUNITY_Phenology & Moisture Stress Tracking]]

## Top bridge nodes
- [[Region-Adaptive Phenology Alignment (RAM)]] - degree 4, connects to 2 communities
- [[Composite Moisture Stress Index (CMSI)]] - degree 4, connects to 1 community
- [[SAR Soil Moisture Index (SMI_SAR)]] - degree 3, connects to 1 community
- [[Split-Window LST Inversion]] - degree 2, connects to 1 community