---
id: false-positive
kind: concept
category: metric
level: 7
aliases: ["false positive"]
---

# False positive / Falso positivo

> **level 7** · *metric* · sources: th_validation · dis_china_floods

**What it is / Qué es.**

- **EN.** A [[pixels|pixel]] or [[samples|sample]] incorrectly classified as belonging to a [[classes|class]] (e.g., [[crop|crop]] or flood) when it actually does not, representing a [[commission|commission error]].
- **ES.** Píxel o muestra clasificado incorrectamente como perteneciente a una clase (p. ej., [[crop|cultivo]] o inundación) cuando en realidad no pertenece, representando un [[commission|error de comisión]].

## Understand these first / Entiende esto primero
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** A false positive occurs when a pixel predicted as a class actually belongs to another in the confusion matrix.
    - **ES.** Un falso positivo ocurre cuando un píxel predicho como una clase realmente pertenece a otra en la matriz de confusión.
- [[commission|Commission]] — *metric*
    - **EN.** False positives correspond to commission errors, where pixels are incorrectly assigned to a class.
    - **ES.** Los falsos positivos corresponden a errores de comisión, donde los píxeles se asignan incorrectamente a una clase.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[commission|Commission]] → [[false-positive|False positive]]
