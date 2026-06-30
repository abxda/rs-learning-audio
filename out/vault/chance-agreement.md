---
id: chance-agreement
kind: concept
category: metric
level: 6
aliases: ["chance agreement"]
---

# Chance agreement / Acuerdo por azar

> **level 6** · *metric* · sources: cy_colombia · cy_colombia

**What it is / Qué es.**

- **EN.** The proportion of [[classification|classification]] agreement that would be expected by random chance, used as a baseline in [[metrics|metrics]] like [[cohen-s-kappa|Cohen’s Kappa]].
- **ES.** La proporción de acuerdo en la [[classification|clasificación]] que se esperaría por azar, utilizada como [[line|línea]] base en [[metrics|métricas]] como el [[cohen-s-kappa|Kappa de Cohen]].

## Understand these first / Entiende esto primero
- [[overall-accuracy|Overall accuracy]] — *metric*
    - **EN.** Chance agreement is a baseline that overall accuracy is compared against in Cohen's Kappa.
    - **ES.** El acuerdo por azar es una línea base con la que se compara la precisión general en el Kappa de Cohen.
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** Chance agreement is the proportion of correct classifications expected by random labeling, derived from the confusion matrix.
    - **ES.** El acuerdo por azar es la proporción de clasificaciones correctas esperadas por etiquetado aleatorio, derivada de la matriz de confusión.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[chance-agreement|Chance agreement]]

## This unlocks / Esto habilita
- [[cohen-s-kappa|Cohen's Kappa]] — Cohen's Kappa corrects observed agreement for chance agreement, giving a reliability measure.
