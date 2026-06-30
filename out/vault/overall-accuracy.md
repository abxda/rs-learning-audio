---
id: overall-accuracy
kind: concept
category: metric
level: 3
aliases: ["overall accuracy"]
---

# Overall accuracy / Precisión general

> **level 3** · *metric* · sources: th_validation · th_validation

**What it is / Qué es.**

- **EN.** The proportion of correctly classified [[pixels|pixels]] or [[samples|samples]] out of the total, calculated as (TP + TN) / (TP + TN + FP + FN). It is a global [[performance|performance]] metric but may be misleading for imbalanced [[classes|classes]].
- **ES.** La proporción de [[pixels|píxeles]] o [[samples|muestras]] correctamente clasificados sobre el total, calculada como (VP + VN) / (VP + VN + FP + FN). Es una métrica de [[yield|rendimiento]] global pero puede ser engañosa para [[classes|clases]] desbalanceadas.

## Understand these first / Entiende esto primero
- [[accuracy|Accuracy]] — *metric*
    - **EN.** Overall accuracy is the proportion of correctly classified pixels or samples out of the total number.
    - **ES.** La precisión general es la proporción de píxeles o muestras clasificados correctamente del número total.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[overall-accuracy|Overall accuracy]]

## This unlocks / Esto habilita
- [[confusion-matrix|Confusion matrix]] — It is calculated from the confusion matrix as the sum of true positives and true negatives divided by total.
- [[kappa-coefficient|Kappa Coefficient]] — Kappa coefficient goes beyond overall accuracy by accounting for chance agreement in classification.
- [[chance-agreement|Chance agreement]] — Chance agreement is a baseline that overall accuracy is compared against in Cohen's Kappa.
