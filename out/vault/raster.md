---
id: raster
kind: concept
category: data
level: 3
aliases: ["raster", "thematic raster"]
---

# Raster / Ráster

> **level 3** · *data* · sources: th_parcel_extraction

**What it is / Qué es.**

- **EN.** A [[data|data]] structure consisting of a [[grid|grid]] of cells ([[pixels|pixels]]) where each cell holds a value representing a measurement, such as [[spectral-reflectance|spectral reflectance]].
- **ES.** Una estructura de [[data|datos]] que consiste en una [[grid|cuadrícula]] de celdas ([[pixels|píxeles]]) donde cada celda contiene un valor que representa una medición, como la [[spectral-reflectance|reflectancia espectral]].

## Understand these first / Entiende esto primero
- [[pixels|Pixels]] — *data*
    - **EN.** A raster is a grid of pixels where each pixel stores a value representing a measurement.
    - **ES.** Un ráster es una cuadrícula de píxeles donde cada píxel almacena un valor que representa una medición.
- [[grid|Grid]] — *data*
    - **EN.** A raster organizes spatial data into a regular grid of cells (pixels) for analysis.
    - **ES.** Un ráster organiza los datos espaciales en una cuadrícula regular de celdas (píxeles) para su análisis.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[images|Images]] → [[tiles|Tiles]] → [[grid|Grid]] → [[raster|Raster]]

## This unlocks / Esto habilita
- [[data-cube|Data cube]] — A data-cube is a multi-temporal raster where each layer is a spatially aligned image at a different date.
- [[zonal-statistics|Zonal Statistics]] — Zonal statistics summarize raster pixel values within each polygon zone to produce per-zone metrics.
