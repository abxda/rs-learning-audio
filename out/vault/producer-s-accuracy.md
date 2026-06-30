---
id: producer-s-accuracy
kind: concept
category: metric
level: 6
aliases: ["producer's accuracy"]
---

# Producer's accuracy / Precisión del productor

> **level 6** · *metric* · sources: th_validation

**What it is / Qué es.**

- **EN.** The [[probability|probability]] that a [[pixels|pixel]] of a given [[classes|class]] on the [[ground|ground]] is correctly classified on the map, calculated as 1 minus the [[omission|omission error]] rate. It measures how well the map represents that class.
- **ES.** La [[probability|probabilidad]] de que un píxel de una clase dada en el [[ground|terreno]] esté correctamente clasificado en el [[map|mapa]], calculada como 1 menos la tasa de [[omission|error de omisión]]. Mide qué tan bien el mapa representa esa clase.

## Understand these first / Entiende esto primero
- [[accuracy|Accuracy]] — *metric*
    - **EN.** Producer's accuracy is the probability that a ground truth pixel is correctly classified on the map.
    - **ES.** La precisión del productor es la probabilidad de que un píxel de verdad terreno esté correctamente clasificado en el mapa.
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** From a confusion matrix, producer's accuracy is computed by dividing correct class pixels by the column total.
    - **ES.** A partir de una matriz de confusión, la precisión del productor se calcula dividiendo los píxeles de clase correctos por el total de la columna.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[producer-s-accuracy|Producer's accuracy]]
