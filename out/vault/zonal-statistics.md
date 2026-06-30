---
id: zonal-statistics
kind: concept
category: method
level: 5
aliases: ["Zonal Statistics", "zonal statistics"]
---

# Zonal Statistics / Estadísticas Zonales

> **level 5** · *method* · sources: uav_agriculture_cook_islands

**What it is / Qué es.**

- **EN.** [[statistical|Statistical]] measures (e.g., mean, standard [[deviation|deviation]]) computed for each [[zone|zone]] or [[polygons|polygon]] in a [[raster|raster]] [[dataset|dataset]], often used to summarize [[pixels|pixel]] [[values|values]] within [[field|field]] [[boundaries|boundaries]] from [[remote-sensing|remote sensing]] [[imagery|imagery]].
- **ES.** Medidas [[statistics|estadísticas]] (ej. media, [[deviation|desviación estándar]]) calculadas para cada [[zone|Zona]] o Polígono en un [[dataset|conjunto de datos]] [[raster|ráster]], a menudo utilizadas para resumir [[values|Valores]] de [[pixels|Píxeles]] dentro de [[boundaries|límites]] de [[field|Campo]] a partir de [[images|Imágenes]] de [[remote-sensing|teledetección]].

## Understand these first / Entiende esto primero
- [[polygons|Polygons]] — *data*
    - **EN.** Zonal statistics compute summary values (e.g., mean NDVI) for each polygon in a vector layer.
    - **ES.** Las estadísticas zonales calculan valores resumidos (p. ej., NDVI medio) para cada polígono en una capa vectorial.
- [[raster|Raster]] — *data*
    - **EN.** Zonal statistics summarize raster pixel values within each polygon zone to produce per-zone metrics.
    - **ES.** Las estadísticas zonales resumen los valores de píxeles ráster dentro de cada zona de polígono para producir métricas por zona.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[area|Area]] → [[land|Land]] → [[field|Field]] → [[parcels|Parcels]] → [[polygons|Polygons]] → [[zonal-statistics|Zonal Statistics]]
