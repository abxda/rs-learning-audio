---
id: temporal-compositing
kind: concept
category: method
level: 3
aliases: ["Temporal Compositing", "temporal compositing"]
---

# Temporal Compositing / Composición temporal

> **level 3** · *method* · sources: th_data_cubes#generating-regular-data-cubes

**What it is / Qué es.**

- **EN.** Temporal compositing is the [[process|process]] of combining multiple [[satellite|satellite]] [[images|images]] over a specified [[time|time]] period into a single image by selecting the best available [[pixels|pixel]] (e.g., [[median|median]], minimum [[cloud|cloud]] [[cover|cover]]) to reduce noise and cloud interference.
- **ES.** La composición temporal es el [[process|proceso]] de combinar múltiples [[satellite-imagery|imágenes satelitales]] durante un período de [[time|tiempo]] específico en una sola imagen seleccionando el mejor píxel disponible (por [[example|ejemplo]], [[median|mediana]], mínima [[cover|cobertura]] de nubes) para reducir ruido e interferencia de nubes.

## Understand these first / Entiende esto primero
- [[time-series|Time series]] — *data*
    - **EN.** Temporal compositing merges multiple images over a time period into a single composite by selecting the best observation per pixel.
    - **ES.** La composición temporal fusiona múltiples imágenes durante un período de tiempo en un único compuesto seleccionando la mejor observación por píxel.
- [[cloud-masking|Cloud Masking]] — *method*
    - **EN.** After cloud masking, temporal compositing combines clear pixels from several dates to produce a cloud-free synthesis.
    - **ES.** Tras el enmascaramiento de nubes, la composición temporal combina píxeles despejados de varias fechas para producir una síntesis sin nubes.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[images|Images]] → [[cloud|Cloud]] → [[cloud-masking|Cloud Masking]] → [[temporal-compositing|Temporal Compositing]]
