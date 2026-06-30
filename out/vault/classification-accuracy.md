---
id: classification-accuracy
kind: concept
category: metric
level: 3
aliases: ["classification accuracy"]
---

# Classification accuracy / Precisión de clasificación

> **level 3** · *metric* · sources: th_validation

**What it is / Qué es.**

- **EN.** Classification accuracy quantifies the degree to which a [[classification-map|classification map]] matches [[reference-datasets|reference data]], measured by [[metrics|metrics]] such as [[overall-accuracy|overall accuracy]], user's [[accuracy|accuracy]], [[producer-s-accuracy|producer's accuracy]], and [[f1-score|F1-score]] from a [[confusion-matrix|confusion matrix]].
- **ES.** La precisión de clasificación cuantifica el grado en que un [[classification-map|mapa de clasificación]] coincide con los [[ground-truth-data|datos de referencia]], medido mediante [[metrics|métricas]] como la [[overall-accuracy|precisión general]], la [[precision|precisión]] del usuario, la [[producer-s-accuracy|precisión del productor]] y la [[f1-score|puntuación F1]] a partir de una [[confusion-matrix|matriz de confusión]].

## Understand these first / Entiende esto primero
- [[accuracy|Accuracy]] — *metric*
    - **EN.** Classification accuracy measures how well a classification map agrees with reference data, extending the concept of accuracy to classification tasks.
    - **ES.** La precisión de clasificación mide cuán bien un mapa de clasificación concuerda con los datos de referencia, extendiendo el concepto de exactitud a tareas de clasificación.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[classification-accuracy|Classification accuracy]]

## This unlocks / Esto habilita
- [[uncertainty|Uncertainty]] — Uncertainty in classification arises from imperfect accuracy; it is quantified by metrics like confidence intervals.
