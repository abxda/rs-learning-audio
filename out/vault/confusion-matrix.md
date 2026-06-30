---
id: confusion-matrix
kind: concept
category: metric
level: 5
aliases: ["confusion matrix"]
---

# Confusion matrix / Matriz de confusión

> **level 5** · *metric* · sources: th_validation#accuracy-assessment-of-classified-images · th_quality_control#validation

**What it is / Qué es.**

- **EN.** A [[table|table]] that compares predicted [[classes|class]] [[label|labels]] (from a map or [[model|model]]) against [[reference|reference]] labels, showing the [[number|number]] of correct and incorrect [[predictions|predictions]] per class. It is the basis for [[accuracy-metrics|accuracy metrics]] such as user's and [[producer-s-accuracy|producer's accuracy]].
- **ES.** Una [[table|tabla]] que compara las etiquetas de clase predichas (de un [[map|mapa]] o [[model|modelo]]) con las etiquetas de [[reference|referencia]], mostrando el [[number|número]] de [[predictions|predicciones]] correctas e incorrectas por clase. Es la base para [[accuracy-metrics|métricas de precisión]] como la [[precision|precisión]] del usuario y del productor.

## Understand these first / Entiende esto primero
- [[classes|Classes]] — *data*
    - **EN.** Each cell of the confusion matrix counts the number of samples for specific predicted versus actual class combinations.
    - **ES.** Cada celda de la matriz de confusión cuenta el número de muestras para combinaciones específicas de clase predicha versus real.
- [[classification|Classification]] — *method*
    - **EN.** A confusion matrix tabulates the agreement between predicted classes from a classification and actual reference classes.
    - **ES.** Una matriz de confusión tabula la concordancia entre las clases predichas de una clasificación y las clases de referencia reales.
- [[accuracy|Accuracy]] — *metric*
    - **EN.** Accuracy metrics like overall accuracy are derived from the confusion matrix by comparing predictions to ground truth.
    - **ES.** Métricas de precisión como la precisión general se derivan de la matriz de confusión al comparar predicciones con verdad terreno.
- [[metrics|Metrics]] — *metric*
    - **EN.** They are derived from a confusion matrix to compute overall accuracy, precision, recall, and F1-score.
    - **ES.** Se derivan de una matriz de confusión para calcular precisión general, precisión, exhaustividad y puntuación F1.
- [[overall-accuracy|Overall accuracy]] — *metric*
    - **EN.** It is calculated from the confusion matrix as the sum of true positives and true negatives divided by total.
    - **ES.** Se calcula a partir de la matriz de confusión como la suma de verdaderos positivos y verdaderos negativos dividida por el total.
- [[accuracy-assessment|Accuracy assessment]] — *method*
    - **EN.** Accuracy assessment is typically based on the confusion matrix comparing predicted vs. reference labels.
    - **ES.** La evaluación de precisión se basa típicamente en la matriz de confusión que compara etiquetas predichas con las de referencia.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]]

## This unlocks / Esto habilita
- [[producer-s-accuracy|Producer's accuracy]] — From a confusion matrix, producer's accuracy is computed by dividing correct class pixels by the column total.
- [[accuracy-metrics|Accuracy metrics]] — From a confusion matrix, many accuracy metrics like producer's and user's accuracy are derived.
- [[confusion-matrices|Confusion matrices]] — Confusion matrices are the plural of confusion matrix; multiple confusion matrices can be used for different regions or classes.
- [[omission|Omission]] — In a confusion matrix, omission corresponds to false negatives for a given class.
- [[commission|Commission]] — In a confusion matrix, commission corresponds to false positives for a given class.
- [[area-weighted-error-matrices|Area-Weighted Error Matrices]] — Area-weighted error matrices weight each cell by the proportion of area that cell represents in the map.
- [[kappa-coefficient|Kappa Coefficient]] — Kappa coefficient measures agreement between classified map and reference data, adjusting for chance agreement.
- [[recall|Recall]] — In a confusion matrix, recall for a class is the proportion of actual positives correctly identified.
- [[false-negative|False negative]] — A false negative occurs when a pixel truly belonging to a class is predicted as another in the confusion matrix.
- [[false-positive|False positive]] — A false positive occurs when a pixel predicted as a class actually belongs to another in the confusion matrix.
- [[chance-agreement|Chance agreement]] — Chance agreement is the proportion of correct classifications expected by random labeling, derived from the confusion matrix.
- [[cohen-s-kappa|Cohen's Kappa]] — Cohen's Kappa quantifies agreement between two raters balancing chance, based on the confusion matrix.
