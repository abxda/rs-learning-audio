---
id: f1-score
kind: concept
category: metric
level: 7
aliases: ["f1-score"]
---

# F1-score / puntuación F1

> **level 7** · *metric* · sources: th_validation#accuracy-assessment-of-classified-images · ct_zimbabwe#accuracy-assessment

**What it is / Qué es.**

- **EN.** The harmonic mean of [[precision|precision]] and [[recall|recall]], providing a single [[measure|measure]] of a [[crop-classification-models|classification model]]'s [[performance|performance]] for a given [[classes|class]]. F1 balances [[commission|commission]] and [[omission|omission]] [[errors|errors]].
- **ES.** Media armónica de la [[precision|precisión]] y la [[recall|exhaustividad]], que proporciona una [[measure|medida]] única del [[yield|rendimiento]] de un [[model|modelo]] de [[classification|clasificación]] para una clase determinada. La puntuación F1 equilibra los [[errors|errores]] de [[commission|comisión]] y [[omission|omisión]].

## Understand these first / Entiende esto primero
- [[precision|Precision]] — *metric*
    - **EN.** F1-score is the harmonic mean of precision and recall, providing a balanced measure of classification performance.
    - **ES.** La puntuación F1 es la media armónica de la precisión y la exhaustividad, proporcionando una medida equilibrada del rendimiento de clasificación.
- [[recall|Recall]] — *metric*
    - **EN.** Recall, together with precision, forms the basis for computing the F1-score in classification evaluation.
    - **ES.** La exhaustividad, junto con la precisión, forma la base para calcular la puntuación F1 en la evaluación de clasificación.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[recall|Recall]] → [[f1-score|F1-score]]
