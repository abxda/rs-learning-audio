---
id: polygons
kind: concept
category: data
level: 4
aliases: ["polygons", "polygon"]
---

# Polygons / Polígonos

> **level 4** · *data* · sources: th_alignment#quality-control-of-gps-traces · uav_agriculture_cook_islands#agricultural-plot-delineation

**What it is / Qué es.**

- **EN.** A [[vector|vector data]] [[type|type]] representing a geographic [[area|area]] enclosed by a boundary. In [[remote-sensing|remote sensing]], [[field|field]] [[parcels|parcels]] are often digitized as polygons for labeling, [[training|training]], and area computation.
- **ES.** Un [[type|tipo]] de dato vectorial que representa un [[area|área]] geográfica encerrada por un límite. En [[remote-sensing|teledetección]], las [[parcels|parcelas]] de [[field|campo]] a menudo se digitalizan como polígonos para etiquetado, [[training|entrenamiento]] y cálculo de área.

## Understand these first / Entiende esto primero
- [[field|Field]] — *phenomenon*
    - **EN.** Polygons are vector boundaries delineating individual fields or parcels in geospatial data.
    - **ES.** Los polígonos son límites vectoriales que delimitan campos o parcelas individuales en datos geoespaciales.
- [[parcels|Parcels]] — *data*
    - **EN.** Parcels are often represented as polygons in geographic information systems for analysis.
    - **ES.** Las parcelas a menudo se representan como polígonos en sistemas de información geográfica para su análisis.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[area|Area]] → [[land|Land]] → [[field|Field]] → [[parcels|Parcels]] → [[polygons|Polygons]]

## This unlocks / Esto habilita
- [[individual-agricultural-plot-polygons|Individual agricultural plot polygons]] — Polygons are vector boundaries used to delineate individual agricultural plots.
- [[vector|Vector]] — A vector object includes points, lines, and polygons; polygons represent field parcels in mapping.
- [[zonal-statistics|Zonal Statistics]] — Zonal statistics compute summary values (e.g., mean NDVI) for each polygon in a vector layer.
- [[boundaries|Boundaries]] — Boundaries are the edges of polygons that delineate agricultural fields or land cover parcels.
