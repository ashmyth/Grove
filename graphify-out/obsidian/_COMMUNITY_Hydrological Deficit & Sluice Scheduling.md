---
type: community
cohesion: 0.40
members: 6
---

# Hydrological Deficit & Sluice Scheduling

**Cohesion:** 0.40 - moderately connected
**Members:** 6 nodes

## Members
- [[8-Day Volumetric Water Deficit (m3ha & mm)]] - document - architecture.md
- [[ECMWF ERA5-Land Meteorology Grids]] - document - architecture.md
- [[Effective Rainfall Model (Peff = 0.8P)]] - document - architecture.md
- [[FAO-56 Dynamic Crop Coefficients (Kc)]] - document - architecture.md
- [[Hargreaves-Samani ET0 Engine]] - document - architecture.md
- [[Sluice Release Discharge Scheduler (Q = Vt)]] - document - architecture.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Hydrological_Deficit__Sluice_Scheduling
SORT file.name ASC
```

## Connections to other communities
- 1 edge to [[_COMMUNITY_Satellite Remote Sensing & Preprocessing_2]]
- 1 edge to [[_COMMUNITY_Satellite Remote Sensing & Preprocessing]]
- 1 edge to [[_COMMUNITY_Phenology & Moisture Stress Tracking]]

## Top bridge nodes
- [[ECMWF ERA5-Land Meteorology Grids]] - degree 3, connects to 1 community
- [[FAO-56 Dynamic Crop Coefficients (Kc)]] - degree 2, connects to 1 community
- [[Sluice Release Discharge Scheduler (Q = Vt)]] - degree 2, connects to 1 community