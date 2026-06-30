---
id: time-series
kind: concept
category: data
level: 1
aliases: ["series", "time series"]
---

# Time series / Serie temporal

> **level 1** · *data* · sources: th_data_cubes · th_lucc

**What it is / Qué es.**

- **EN.** A sequence of [[data|data]] [[points|points]] collected at successive, often equally spaced, [[time|time]] intervals, used to analyze temporal [[patterns|patterns]] such as [[crop|crop]] [[growth|growth]].
- **ES.** Una secuencia de [[points|puntos]] de [[data|datos]] recopilados en intervalos de [[time|tiempo]] sucesivos, a menudo igualmente espaciados, utilizados para analizar [[patterns|patrones]] temporales como el [[growth|crecimiento]] de cultivos.

## Understand these first / Entiende esto primero
- [[images|Images]] — *data*
    - **EN.** A satellite image time series combines multiple images of the same location taken at different times.
    - **ES.** Una serie temporal de imágenes satelitales combina múltiples imágenes de la misma ubicación tomadas en diferentes momentos.
- [[time|Time]] — *primitive*
    - **EN.** A time series is a sequence of data points collected at successive, often equally spaced, times.
    - **ES.** Una serie temporal es una secuencia de puntos de datos recopilados en tiempos sucesivos, a menudo igualmente espaciados.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[images|Images]] → [[time-series|Time series]]

## This unlocks / Esto habilita
- [[satellite-image-time-series|Satellite image time series]] — A satellite image time series is a specific type of time series where each observation is an image capturing land surface conditions.
- [[patterns|Patterns]] — A time series reveals seasonal patterns, which we can generalize into idealized patterns for each land cover class.
- [[better-reference-data-series|Better reference data series]] — A better reference data series may include temporal information to capture phenological patterns.
- [[continuous-monitoring|Continuous monitoring]] — It relies on dense time series to detect subtle temporal changes over the entire season.
- [[temporal-pattern|Temporal pattern]] — A temporal pattern is a recurring sequence or trend observed in a satellite image time series.
- [[yield-forecasting|Yield forecasting]] — Satellite image time series capture temporal crop growth patterns essential for yield forecasting models.
- [[phenological-patterns|Phenological patterns]] — Satellite time series data reveal phenological patterns through changes in vegetation indices over the growing season.
- [[temporal-compositing|Temporal Compositing]] — Temporal compositing merges multiple images over a time period into a single composite by selecting the best observation per pixel.
- [[spectral-temporal-signatures|Spectral-Temporal Signatures]] — Spectral-temporal signatures are the unique patterns of spectral indices over time for a given land cover.
- [[time-series-analysis|Time series analysis]] — Time series analysis focuses on sequences of data points collected at successive times.
- [[som|SOM]] — SOM organizes input time series into clusters, preserving topological relationships for pattern discovery.
