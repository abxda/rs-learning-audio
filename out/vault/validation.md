---
id: validation
kind: concept
category: method
level: 3
aliases: ["validation"]
---

# Validation / Validación

> **level 3** · *method* · sources: th_validation

**What it is / Qué es.**

- **EN.** The [[process|process]] of assessing the [[accuracy|accuracy]] of a [[classification|classification]] or [[model|model]] by comparing its [[predictions|predictions]] against independent [[reference-datasets|reference data]].
- **ES.** El [[process|proceso]] de evaluar la [[accuracy|exactitud]] de una [[classification|clasificación]] o [[model|modelo]] comparando sus [[predictions|predicciones]] con [[ground-truth-data|datos de referencia]] independientes.

## Understand these first / Entiende esto primero
- [[accuracy|Accuracy]] — *metric*
    - **EN.** Validation assesses the accuracy of a classification by comparing its predictions against independent data.
    - **ES.** La validación evalúa la exactitud de una clasificación comparando sus predicciones con datos independientes.
- [[reference|Reference]] — *primitive*
    - **EN.** Validation uses reference data to check if a map or model correctly reflects ground conditions.
    - **ES.** La validación utiliza datos de referencia para verificar si un mapa o modelo refleja correctamente las condiciones del terreno.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]]

## This unlocks / Esto habilita
- [[map-validation|Map Validation]] — Map validation is the process of assessing a map's accuracy by comparing it to reference data.
- [[statistics-production|Statistics production]] — It includes validation steps to ensure the accuracy and reliability of the produced statistics.
- [[model-generalization-capabilities|Model generalization capabilities]] — Generalization is assessed by validating the model on independent datasets from different regions or times.
- [[accuracy-assessment|Accuracy assessment]] — Accuracy assessment uses validation data independent of training to compute error metrics.
- [[data-division|Data Division]] — Data division reserves a validation set to tune model parameters and prevent overfitting.
- [[model-evaluation|Model evaluation]] — Model evaluation uses validation datasets to compute accuracy metrics and detect overfitting.
