---
id: processing
kind: concept
category: method
level: 1
aliases: ["processing"]
---

# Processing / Procesamiento

> **level 1** · *method* · sources: th_data_sources

**What it is / Qué es.**

- **EN.** Processing refers to the steps applied to raw [[satellite-data|satellite data]] to make it suitable for [[analysis|analysis]], including geometric and [[radiometric-corrections|radiometric corrections]], [[cloud-masking|cloud masking]], and conversion to [[surface-reflectance|surface reflectance]] or backscatter [[values|values]].
- **ES.** El procesamiento se refiere a los pasos aplicados a los [[satellite-data|datos satelitales]] crudos para hacerlos aptos para el [[analysis|análisis]], incluyendo correcciones geométricas y radiométricas, [[cloud-masking|enmascaramiento de nubes]] y conversión a [[surface-reflectance|reflectancia superficial]] o [[values|valores]] de retrodispersión.

## Understand these first / Entiende esto primero
- [[data|Data]] — *primitive*
    - **EN.** By applying a series of operations to raw data, we transform it into a more useful form.
    - **ES.** Al aplicar una serie de operaciones a los datos brutos, los transformamos en una forma más útil.
- [[images|Images]] — *data*
    - **EN.** Raw satellite images are refined through geometric and radiometric corrections during processing.
    - **ES.** Las imágenes satelitales crudas se refinan mediante correcciones geométricas y radiométricas durante el procesamiento.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[processing|Processing]]

## This unlocks / Esto habilita
- [[data-processing|Data processing]] — Data processing is the generic term for the steps applied to any data, including raw satellite data.
- [[high-performance-computing|High-performance computing]] — HPC uses parallel processing and specialized hardware (e.g., GPUs) to accelerate Earth observation workflows.
- [[analysis-ready-data|Analysis Ready Data]] — ARD is produced by applying geometric, radiometric, and atmospheric corrections to raw satellite imagery.
- [[atmospheric-correction|Atmospheric correction]] — Atmospheric correction is a processing step that removes scattering and absorption effects from satellite data.
