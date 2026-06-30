---
id: area-weighted-error-matrices
kind: concept
category: metric
level: 6
aliases: ["Area-Weighted Error Matrices", "area-weighted error matrices"]
---

# Area-Weighted Error Matrices / Matrices de error ponderadas por área

> **level 6** · *metric* · sources: th_validation#accuracy-assessment-of-classified-images

**What it is / Qué es.**

- **EN.** An [[area|area]]-weighted error matrix adjusts the standard [[confusion-matrix|confusion matrix]] by weighting each cell by the proportion of area mapped as that [[classes|class]], providing unbiased [[accuracy|accuracy]] and [[area-statistics|area estimates]].
- **ES.** Una matriz de error ponderada por [[area|área]] ajusta la [[confusion-matrix|matriz de confusión]] estándar ponderando cada celda por la proporción de área mapeada como esa clase, proporcionando [[estimates|estimaciones]] de [[accuracy|exactitud]] y área insesgadas.

## Understand these first / Entiende esto primero
- [[area|Area]] — *metric*
    - **EN.** Area weighting adjusts confusion matrices by the spatial extent of each class to reduce bias in accuracy metrics.
    - **ES.** La ponderación por área ajusta las matrices de confusión según la extensión espacial de cada clase para reducir el sesgo en las métricas de precisión.
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** Area-weighted error matrices weight each cell by the proportion of area that cell represents in the map.
    - **ES.** Las matrices de error ponderadas por área ponderan cada celda según la proporción de área que representa en el mapa.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[area-weighted-error-matrices|Area-Weighted Error Matrices]]
