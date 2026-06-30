---
id: omission
kind: concept
category: metric
level: 6
aliases: ["Omission", "omission", "omission error"]
---

# Omission / Omisión

> **level 6** · *metric* · sources: th_validation#accuracy-assessment-of-classified-images

**What it is / Qué es.**

- **EN.** Omission error ([[false-negative|false negative]]) occurs when a [[pixels|pixel]] or [[area|area]] that belongs to a [[classes|class]] in reality is not classified as that class by the map, leading to [[underestimation|underestimation]] of that class's extent.
- **ES.** El error de omisión ([[false-negative|falso negativo]]) ocurre cuando un píxel o [[area|área]] que pertenece a una clase en la realidad no es clasificado como esa clase por el [[map|mapa]], lo que lleva a una [[underestimation|subestimación]] de la extensión de esa clase.

## Understand these first / Entiende esto primero
- [[classification|Classification]] — *method*
    - **EN.** Omission error occurs when a pixel belonging to a class on the ground is missed in the classified map.
    - **ES.** El error de omisión ocurre cuando un píxel perteneciente a una clase en el terreno se omite en el mapa clasificado.
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** In a confusion matrix, omission corresponds to false negatives for a given class.
    - **ES.** En una matriz de confusión, la omisión corresponde a falsos negativos para una clase determinada.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[omission|Omission]]

## This unlocks / Esto habilita
- [[false-negative|False negative]] — False negatives correspond to omission errors, where true class pixels are missed in the map.
