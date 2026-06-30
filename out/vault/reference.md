---
id: reference
kind: concept
category: primitive
level: 2
aliases: ["reference"]
---

# Reference / Referencia

> **level 2** · *primitive* · sources: th_quality_control

**What it is / Qué es.**

- **EN.** [[reference-datasets|Reference data]] are [[ground-truth|ground-truth]] observations used to train and validate [[crop-classification-models|classification models]]. They include [[field-surveys|field surveys]], photo-interpreted [[samples|samples]], or administrative records that provide accurate [[label|labels]] for [[land-cover|land cover]] or [[crop-types|crop types]].
- **ES.** Los [[ground-truth-data|datos de referencia]] son observaciones de [[ground-truth|verdad terreno]] utilizadas para entrenar y validar modelos de [[classification|clasificación]]. Incluyen [[ground-surveys|encuestas de campo]], [[samples|muestras]] fotointerpretadas o registros administrativos que proporcionan etiquetas precisas para la [[land-cover|cobertura del suelo]] o [[crop-types|tipos de cultivos]].

## Understand these first / Entiende esto primero
- [[samples|Samples]] — *data*
    - **EN.** Labeled samples from the field form the reference dataset for training and validation.
    - **ES.** Las muestras etiquetadas de campo conforman el conjunto de datos de referencia para entrenamiento y validación.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[reference|Reference]]

## This unlocks / Esto habilita
- [[validation|Validation]] — Validation uses reference data to check if a map or model correctly reflects ground conditions.
- [[data-scarce-regions|Data scarce regions]] — In data-scarce regions, reference data are sparse, making it difficult to train robust classification models.
- [[ground|Ground]] — Reference data consists of ground observations used to label satellite image samples.
