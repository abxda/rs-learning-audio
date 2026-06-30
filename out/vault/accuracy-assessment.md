---
id: accuracy-assessment
kind: concept
category: method
level: 4
aliases: ["accuracy assessment"]
---

# Accuracy assessment / Evaluación de precisión

> **level 4** · *method* · sources: th_validation · th_validation

**What it is / Qué es.**

- **EN.** The [[process|process]] of evaluating the [[quality|quality]] of a [[classified-map|classified map]] by comparing it to [[reference-datasets|reference data]], often using [[metrics|metrics]] like [[overall-accuracy|overall accuracy]], user's [[accuracy|accuracy]], and [[producer-s-accuracy|producer's accuracy]].
- **ES.** El [[process|proceso]] de evaluar la [[quality|calidad]] de un [[classified-map|mapa clasificado]] comparándolo con [[ground-truth-data|datos de referencia]], utilizando a menudo [[metrics|métricas]] como la [[overall-accuracy|precisión general]], la [[precision|precisión]] del usuario y la [[producer-s-accuracy|precisión del productor]].

## Understand these first / Entiende esto primero
- [[classification|Classification]] — *method*
    - **EN.** Accuracy assessment evaluates how correctly a classification assigns labels to pixels or objects.
    - **ES.** La evaluación de precisión evalúa qué tan correctamente una clasificación asigna etiquetas a píxeles u objetos.
- [[accuracy|Accuracy]] — *metric*
    - **EN.** Accuracy assessment quantifies the overall accuracy of a classified map through comparison with reference.
    - **ES.** La evaluación de precisión cuantifica la exactitud general de un mapa clasificado mediante comparación con referencia.
- [[validation|Validation]] — *method*
    - **EN.** Accuracy assessment uses validation data independent of training to compute error metrics.
    - **ES.** La evaluación de precisión utiliza datos de validación independientes del entrenamiento para calcular métricas de error.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]]

## This unlocks / Esto habilita
- [[validation-datasets|Validation datasets]] — They enable accuracy assessment by providing ground truth for comparison with model predictions.
- [[confusion-matrix|Confusion matrix]] — Accuracy assessment is typically based on the confusion matrix comparing predicted vs. reference labels.
