---
id: prediction-probabilities
kind: concept
category: metric
level: 6
aliases: ["Prediction Probabilities", "prediction probabilities"]
---

# Prediction Probabilities / Probabilidades de predicción

> **level 6** · *metric* · sources: th_uncertainty#measuring-uncertainty

**What it is / Qué es.**

- **EN.** Prediction probabilities are the output [[values|values]] from a [[crop-classification-models|classification model]] that represent the estimated likelihood that a [[pixels|pixel]] belongs to each possible [[classes|class]], typically ranging from 0 to 1.
- **ES.** Las probabilidades de predicción son los [[values|valores]] de salida de un [[model|modelo]] de [[classification|clasificación]] que representan la [[probability|probabilidad]] estimada de que un píxel pertenezca a cada clase posible, típicamente en un [[range|rango]] de 0 a 1.

## Understand these first / Entiende esto primero
- [[machine-learning|Machine learning]] — *method*
    - **EN.** Machine learning models often produce prediction probabilities for each class, indicating confidence.
    - **ES.** Los modelos de aprendizaje automático a menudo producen probabilidades de predicción para cada clase, indicando confianza.
- [[classification-algorithm|Classification algorithm]] — *method*
    - **EN.** Classification algorithms output prediction probabilities representing the likelihood of a pixel belonging to each class.
    - **ES.** Los algoritmos de clasificación generan probabilidades de predicción que representan la probabilidad de que un píxel pertenezca a cada clase.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[training|Training]] → [[machine-learning|Machine learning]] → [[algorithm|Algorithm]] → [[classification-algorithm|Classification algorithm]] → [[prediction-probabilities|Prediction Probabilities]]

## This unlocks / Esto habilita
- [[uncertainty|Uncertainty]] — Uncertainty can be expressed through prediction probabilities, which indicate how confident the model is.
