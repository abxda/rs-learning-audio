---
id: commission
kind: concept
category: metric
level: 6
aliases: ["Commission", "commission", "commission error"]
---

# Commission / Comisión

> **level 6** · *metric* · sources: th_validation#accuracy-assessment-of-classified-images

**What it is / Qué es.**

- **EN.** Commission error ([[false-positive|false positive]]) occurs when a [[pixels|pixel]] or [[area|area]] is incorrectly assigned to a [[classes|class]] in the map when it does not belong to that class in reality, leading to [[overestimation|overestimation]].
- **ES.** El error de comisión ([[false-positive|falso positivo]]) ocurre cuando un píxel o [[area|área]] se asigna incorrectamente a una clase en el [[map|mapa]] cuando no pertenece a esa clase en la realidad, lo que lleva a una [[overestimation|sobreestimación]].

## Understand these first / Entiende esto primero
- [[classification|Classification]] — *method*
    - **EN.** Commission error occurs when a pixel is incorrectly labeled as a class it does not belong to.
    - **ES.** El error de comisión ocurre cuando un píxel se etiqueta incorrectamente como una clase a la que no pertenece.
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** In a confusion matrix, commission corresponds to false positives for a given class.
    - **ES.** En una matriz de confusión, la comisión corresponde a falsos positivos para una clase determinada.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[commission|Commission]]

## This unlocks / Esto habilita
- [[false-positive|False positive]] — False positives correspond to commission errors, where pixels are incorrectly assigned to a class.
