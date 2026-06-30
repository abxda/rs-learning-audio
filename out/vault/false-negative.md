---
id: false-negative
kind: concept
category: metric
level: 7
aliases: ["false negative"]
---

# False negative / Falso negativo

> **level 7** · *metric* · sources: th_validation · dis_china_floods

**What it is / Qué es.**

- **EN.** A [[pixels|pixel]] or [[samples|sample]] incorrectly classified as not belonging to a [[classes|class]] (e.g., [[crop|crop]] or flood) when it actually does, representing an [[omission|omission error]].
- **ES.** Píxel o muestra clasificado incorrectamente como no perteneciente a una clase (p. ej., [[crop|cultivo]] o inundación) cuando en realidad sí pertenece, representando un [[omission|error de omisión]].

## Understand these first / Entiende esto primero
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** A false negative occurs when a pixel truly belonging to a class is predicted as another in the confusion matrix.
    - **ES.** Un falso negativo ocurre cuando un píxel que realmente pertenece a una clase se predice como otra en la matriz de confusión.
- [[omission|Omission]] — *metric*
    - **EN.** False negatives correspond to omission errors, where true class pixels are missed in the map.
    - **ES.** Los falsos negativos corresponden a errores de omisión, donde se omiten píxeles de clase verdadera en el mapa.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[omission|Omission]] → [[false-negative|False negative]]
