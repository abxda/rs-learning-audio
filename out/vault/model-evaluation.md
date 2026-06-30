---
id: model-evaluation
kind: concept
category: method
level: 4
aliases: ["Model evaluation"]
---

# Model evaluation / Evaluación de modelos

> **level 4** · *method* · sources: th_validation#accuracy-assessment-of-classified-images

**What it is / Qué es.**

- **EN.** The [[process|process]] of assessing a [[crop-classification-models|classification model]]'s [[performance|performance]] using [[metrics|metrics]] like [[accuracy|accuracy]], [[precision|precision]], [[recall|recall]], and [[f1-score|F1-score]] on a [[validation|validation]] [[dataset|dataset]].
- **ES.** El [[process|proceso]] de evaluar el [[yield|rendimiento]] de un [[model|modelo]] de [[classification|clasificación]] utilizando [[metrics|métricas]] como [[accuracy|exactitud]], [[precision|precisión]], [[recall|exhaustividad]] y [[f1-score|puntuación F1]] en un [[dataset|conjunto de datos]] de [[validation|validación]].

## Understand these first / Entiende esto primero
- [[model|Model]] — *method*
    - **EN.** Model evaluation assesses how well a trained model performs on unseen data.
    - **ES.** La evaluación de modelos evalúa qué tan bien se desempeña un modelo entrenado con datos no vistos.
- [[performance|Performance]] — *metric*
    - **EN.** Model evaluation measures the performance of a model using quantitative metrics.
    - **ES.** La evaluación de modelos mide el rendimiento de un modelo utilizando métricas cuantitativas.
- [[validation|Validation]] — *method*
    - **EN.** Model evaluation uses validation datasets to compute accuracy metrics and detect overfitting.
    - **ES.** La evaluación de modelos utiliza conjuntos de datos de validación para calcular métricas de precisión y detectar sobreajuste.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[performance|Performance]] → [[model-evaluation|Model evaluation]]

## This unlocks / Esto habilita
- [[model-development|Model Development]] — Model development includes model evaluation to assess performance and guide improvements.
