---
id: precision
kind: concept
category: metric
level: 3
aliases: ["precision"]
---

# Precision / Precisión

> **level 3** · *metric* · sources: th_validation#accuracy-assessment-of-classified-images

**What it is / Qué es.**

- **EN.** In [[classification|classification]], the fraction of [[pixels|pixels]] predicted as a given [[classes|class]] that actually belong to that class in the [[reference-datasets|reference data]].
- **ES.** En [[classification|clasificación]], la fracción de [[pixels|píxeles]] predichos como una clase dada que realmente pertenecen a esa clase en los [[ground-truth-data|datos de referencia]].

## Understand these first / Entiende esto primero
- [[classification|Classification]] — *method*
    - **EN.** Precision (user's accuracy) measures how many of the pixels predicted as a class truly belong to that class.
    - **ES.** La precisión (exactitud del usuario) mide cuántos de los píxeles predichos como una clase realmente pertenecen a esa clase.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[classification|Classification]] → [[precision|Precision]]

## This unlocks / Esto habilita
- [[accuracy-metrics|Accuracy metrics]] — Precision is a classification metric derived from the confusion matrix.
- [[f1-score|F1-score]] — F1-score is the harmonic mean of precision and recall, providing a balanced measure of classification performance.
