---
id: undersampling
kind: concept
category: method
level: 5
aliases: ["undersampling"]
---

# Undersampling / Submuestreo

> **level 5** · *method* · sources: th_quality_control · th_quality_control

**What it is / Qué es.**

- **EN.** A technique that reduces the [[number|number]] of [[samples|samples]] from overrepresented [[classes|classes]] to balance the [[training-dataset|training dataset]], often using [[self-organizing-maps|Self-Organizing Maps]] (SOM).
- **ES.** Técnica que reduce el [[number|número]] de [[samples|muestras]] de [[classes|clases]] sobrerrepresentadas para equilibrar el [[training-dataset|conjunto de datos de entrenamiento]], a menudo empleando [[self-organizing-maps|Mapas Autoorganizados]] (SOM).

## Understand these first / Entiende esto primero
- [[training-dataset|Training dataset]] — *data*
    - **EN.** Undersampling reduces the number of samples in overrepresented classes to balance the training dataset.
    - **ES.** El submuestreo reduce el número de muestras en clases sobrerrepresentadas para equilibrar el conjunto de datos de entrenamiento.
- [[sample-balancing|Sample balancing]] — *method*
    - **EN.** It is a sample balancing technique that alleviates class imbalance by removing majority class samples.
    - **ES.** Es una técnica de balanceo de muestra que alivia el desequilibrio de clases eliminando muestras de la clase mayoritaria.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[label|Label]] → [[training-samples|Training samples]] → [[sample-balancing|Sample balancing]] → [[undersampling|Undersampling]]
