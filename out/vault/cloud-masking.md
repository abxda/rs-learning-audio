---
id: cloud-masking
kind: concept
category: method
level: 2
aliases: ["Cloud Masking", "cloud masking"]
---

# Cloud Masking / Enmascaramiento de nubes

> **level 2** · *method* · sources: th_data_sources#ard-image-collections

**What it is / Qué es.**

- **EN.** Cloud masking is the [[process|process]] of identifying and removing [[pixels|pixels]] affected by clouds or [[cloud|cloud]] shadows in [[satellite-imagery|satellite imagery]], often using spectral tests or pre-computed [[quality|quality]] [[bands|bands]], to ensure clear observations.
- **ES.** El enmascaramiento de nubes es el [[process|proceso]] de identificar y eliminar [[pixels|píxeles]] afectados por nubes o sombras de nubes en [[satellite-imagery|imágenes satelitales]], a menudo usando pruebas espectrales o [[bands|bandas]] de [[quality|calidad]] precalculadas, para garantizar observaciones claras.

## Understand these first / Entiende esto primero
- [[images|Images]] — *data*
    - **EN.** Cloud masking identifies and removes cloudy pixels in satellite images to ensure clear observations.
    - **ES.** El enmascaramiento de nubes identifica y elimina píxeles nubosos en imágenes satelitales para asegurar observaciones claras.
- [[cloud|Cloud]] — *phenomenon*
    - **EN.** Cloud masking uses cloud detection algorithms to remove cloud-affected pixels from satellite imagery.
    - **ES.** El enmascaramiento de nubes utiliza algoritmos de detección de nubes para eliminar píxeles afectados por nubes de las imágenes satelitales.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[images|Images]] → [[cloud|Cloud]] → [[cloud-masking|Cloud Masking]]

## This unlocks / Esto habilita
- [[temporal-compositing|Temporal Compositing]] — After cloud masking, temporal compositing combines clear pixels from several dates to produce a cloud-free synthesis.
