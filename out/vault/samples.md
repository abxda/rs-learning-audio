---
id: samples
kind: concept
category: data
level: 1
aliases: ["samples", "sample"]
---

# Samples / Muestras

> **level 1** · *data* · sources: th_quality_control

**What it is / Qué es.**

- **EN.** Individual observations with known [[label|labels]] used to train or validate [[machine-learning-models|machine learning models]], typically consisting of spectral and temporal [[data|data]].
- **ES.** Observaciones individuales con etiquetas conocidas utilizadas para entrenar o validar [[machine-learning-models|modelos de aprendizaje automático]], que consisten típicamente en [[data|datos]] espectrales y temporales.

## Understand these first / Entiende esto primero
- [[data|Data]] — *primitive*
    - **EN.** Samples are individual data points with known labels used for training or validation.
    - **ES.** Las muestras son puntos de datos individuales con etiquetas conocidas utilizados para entrenamiento o validación.
- [[classes|Classes]] — *data*
    - **EN.** Samples are assigned to classes, providing ground truth for supervised learning.
    - **ES.** Las muestras se asignan a clases, proporcionando verdad terreno para el aprendizaje supervisado.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]]

## This unlocks / Esto habilita
- [[classification|Classification]] — Labeled samples train the classification model to recognize class patterns.
- [[accuracy|Accuracy]] — Accuracy is computed by comparing predicted labels to known sample labels.
- [[training|Training]] — Training fits a model to labeled samples so it learns to classify new data.
- [[label|Label]] — Labels are assigned to each sample in the training set, providing known categories for classification.
- [[field-samples|Field samples]] — Field samples are samples collected directly from agricultural fields during ground surveys.
- [[instances|Instances]] — Instances are individual training or validation data points, such as a single pixel's time series.
- [[training-samples|Training samples]] — Training samples are a subset of samples with known labels used to teach a machine learning model.
- [[random-training-testing-datasets|Random training testing datasets]] — Random training-testing datasets randomly partition samples into training and testing sets.
- [[labeled-samples|Labeled samples]] — Labeled samples are observations that have been assigned a ground truth class by an expert.
- [[representativeness|Representativeness]] — Representativeness ensures that the collected samples reflect the diversity of the entire population for accurate estimates.
- [[reference-samples|Reference samples]] — Reference samples are a subset of samples with known ground truth labels used for training or validating models.
- [[sample-balancing|Sample balancing]] — Sample balancing techniques (e.g., oversampling, undersampling) create a more balanced training dataset.
- [[model-training|Model training]] — During model training, the algorithm learns to map input features to output classes using labeled samples.
- [[reference|Reference]] — Labeled samples from the field form the reference dataset for training and validation.
- [[extensive-ground-samples|Extensive ground samples]] — Extensive ground samples are a large number of labeled samples collected in the field.
