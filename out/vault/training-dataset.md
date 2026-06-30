---
id: training-dataset
kind: concept
category: data
level: 3
aliases: ["training dataset", "training data"]
---

# Training dataset / Conjunto de datos de entrenamiento

> **level 3** · *data* · sources: th_quality_control

**What it is / Qué es.**

- **EN.** A training dataset is a set of [[labeled-samples|labeled samples]] used to teach a [[machine-learning|machine learning]] [[model|model]] to recognize [[patterns|patterns]]. In [[remote-sensing|remote sensing]], it consists of [[satellite-image-time-series|satellite image time series]] with known [[land-cover|land cover]] or [[crop-types|crop type]] [[label|labels]].
- **ES.** Un conjunto de datos de entrenamiento es un [[set|conjunto]] de [[labeled-samples|muestras etiquetadas]] utilizado para enseñar a un [[model|modelo]] de [[machine-learning|aprendizaje automático]] a reconocer [[patterns|patrones]]. En [[remote-sensing|teledetección]], consiste en [[satellite-image-time-series|series temporales de imágenes satelitales]] con etiquetas conocidas de [[land-cover|cobertura del suelo]] o [[type|tipo]] de [[crop|cultivo]].

## Understand these first / Entiende esto primero
- [[dataset|Dataset]] — *data*
    - **EN.** A training dataset is a labeled dataset used to train models, extending the general dataset concept.
    - **ES.** Un conjunto de datos de entrenamiento es un conjunto de datos etiquetado utilizado para entrenar modelos, ampliando el concepto general de conjunto de datos.
- [[training|Training]] — *method*
    - **EN.** A training dataset is the data used during the training process of a machine learning model.
    - **ES.** Un conjunto de datos de entrenamiento son los datos utilizados durante el proceso de entrenamiento de un modelo de aprendizaje automático.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[training|Training]] → [[training-dataset|Training dataset]]

## This unlocks / Esto habilita
- [[better-reference-data-series|Better reference data series]] — A better reference data series serves as an improved training dataset for classification models.
- [[quality-control|Quality Control]] — Quality control of training data ensures samples are accurate and representative before model training.
- [[undersampling|Undersampling]] — Undersampling reduces the number of samples in overrepresented classes to balance the training dataset.
- [[labeled-samples|Labeled samples]] — A training dataset consists of labeled samples that serve as ground truth for supervised learning.
