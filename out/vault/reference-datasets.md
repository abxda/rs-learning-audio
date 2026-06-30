---
id: reference-datasets
kind: concept
category: data
level: 2
aliases: ["reference datasets", "reference data"]
---

# Reference datasets / Conjuntos de datos de referencia

> **level 2** · *data* · sources: th_validation

**What it is / Qué es.**

- **EN.** Collections of [[ground-truth|ground-truth]] observations used for [[training|training]] and validating [[crop-classification-models|classification models]]. They must be collected independently of the [[classification-process|classification process]] and accurately labeled.
- **ES.** Colecciones de observaciones de [[ground-truth|verdad terreno]] utilizadas para entrenar y validar modelos de [[classification|clasificación]]. Deben recolectarse independientemente del [[classification-process|proceso de clasificación]] y etiquetarse con [[precision|precisión]].

## Understand these first / Entiende esto primero
- [[dataset|Dataset]] — *data*
    - **EN.** They are curated datasets containing labeled samples for the study area.
    - **ES.** Son conjuntos de datos seleccionados que contienen muestras etiquetadas para el área de estudio.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[dataset|Dataset]] → [[reference-datasets|Reference datasets]]

## This unlocks / Esto habilita
- [[ground-truth|Ground-truth]] — Reference datasets are collections of ground-truth observations used to train and validate models.
- [[labeled-samples|Labeled samples]] — Each reference dataset consists of labeled samples that specify the correct class for a location.
- [[worldcereal-reference-data-module|WorldCereal Reference Data Module]] — The WorldCereal Reference Data Module provides a framework for harmonizing and sharing reference datasets for crop mapping.
- [[validation-datasets|Validation datasets]] — Validation datasets are independent reference datasets used to assess the accuracy of a classification model.
