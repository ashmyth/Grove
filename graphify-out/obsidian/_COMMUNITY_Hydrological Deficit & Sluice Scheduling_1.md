---
type: community
cohesion: 0.50
members: 4
---

# Hydrological Deficit & Sluice Scheduling

**Cohesion:** 0.50 - moderately connected
**Members:** 4 nodes

## Members
- [[Canal Command Engineer  Sluice Operator]] - document - prd.md
- [[CanalAdvisory Component (Sluice Tables & Gauges)]] - document - architecture.md
- [[ExportAdvisory Component (PDF  CSV)]] - document - architecture.md
- [[GET apiv1canalsadvisories]] - document - architecture.md

## Live Query (requires Dataview plugin)

```dataview
TABLE source_file, type FROM #community/Hydrological_Deficit__Sluice_Scheduling
SORT file.name ASC
```

## Connections to other communities
- 2 edges to [[_COMMUNITY_Multimodal AIML & Foundation Models]]
- 1 edge to [[_COMMUNITY_Phenology & Moisture Stress Tracking]]

## Top bridge nodes
- [[CanalAdvisory Component (Sluice Tables & Gauges)]] - degree 3, connects to 1 community
- [[GET apiv1canalsadvisories]] - degree 2, connects to 1 community
- [[ExportAdvisory Component (PDF  CSV)]] - degree 2, connects to 1 community