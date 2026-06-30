---
id: recall
kind: concept
category: metric
level: 6
aliases: ["recall"]
---

# Recall / Exhaustividad

> **level 6** · *metric* · sources: th_validation · cy_colombia

**What it is / Qué es.**

- **EN.** The proportion of actual positive [[instances|instances]] correctly identified by a classifier, also called [[producer-s-accuracy|Producer's Accuracy]]. It measures [[omission|omission]] [[errors|errors]].
- **ES.** La proporción de [[instances|instancias]] positivas reales identificadas correctamente por un clasificador, también llamada [[producer-s-accuracy|precisión del productor]]. Mide los [[errors|errores]] de [[omission|omisión]].

## Understand these first / Entiende esto primero
- [[accuracy|Accuracy]] — *metric*
    - **EN.** Recall is derived from the confusion matrix as the true positives divided by the sum of true positives and false negatives.
    - **ES.** La exhaustividad se deriva de la matriz de confusión como los verdaderos positivos divididos por la suma de verdaderos positivos y falsos negativos.
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** In a confusion matrix, recall for a class is the proportion of actual positives correctly identified.
    - **ES.** En una matriz de confusión, la exhaustividad para una clase es la proporción de positivos reales correctamente identificados.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[recall|Recall]]

## This unlocks / Esto habilita
- [[f1-score|F1-score]] — Recall, together with precision, forms the basis for computing the F1-score in classification evaluation.
