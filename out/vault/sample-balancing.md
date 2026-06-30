---
id: sample-balancing
kind: concept
category: method
level: 4
aliases: ["sample balancing"]
---

# Sample balancing / Balanceo de muestra

> **level 4** · *method* · sources: th_quality_control

**What it is / Qué es.**

- **EN.** Techniques to adjust an imbalanced [[training-dataset|training dataset]], such as [[oversampling|oversampling]] minority [[classes|classes]] (e.g., [[smote|SMOTE]]) or [[undersampling|undersampling]] majority classes, to improve classifier [[performance|performance]] on less frequent categories.
- **ES.** Técnicas para ajustar un [[training-dataset|conjunto de datos de entrenamiento]] desequilibrado, como el [[oversampling|sobremuestreo]] de [[classes|clases]] minoritarias (p. ej., [[smote|SMOTE]]) o el [[undersampling|submuestreo]] de clases mayoritarias, para mejorar el [[yield|rendimiento]] del clasificador en categorías menos frecuentes.

## Understand these first / Entiende esto primero
- [[samples|Samples]] — *data*
    - **EN.** Sample balancing techniques (e.g., oversampling, undersampling) create a more balanced training dataset.
    - **ES.** Las técnicas de balanceo de muestra (p. ej., sobremuestreo, submuestreo) crean un conjunto de datos de entrenamiento más equilibrado.
- [[training-samples|Training samples]] — *data*
    - **EN.** Sample balancing adjusts the class distribution in training samples to avoid bias toward majority classes.
    - **ES.** El balanceo de muestra ajusta la distribución de clases en las muestras de entrenamiento para evitar sesgos hacia clases mayoritarias.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[label|Label]] → [[training-samples|Training samples]] → [[sample-balancing|Sample balancing]]

## This unlocks / Esto habilita
- [[undersampling|Undersampling]] — It is a sample balancing technique that alleviates class imbalance by removing majority class samples.
