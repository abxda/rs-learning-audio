---
id: accuracy
kind: concept
category: metric
level: 2
aliases: ["accuracy"]
---

# Accuracy / Exactitud

> **level 2** · *metric* · sources: th_validation

**What it is / Qué es.**

- **EN.** A metric of how correctly a [[classification|classification]] or [[estimation|estimation]] matches reality, typically quantified as [[overall-accuracy|overall accuracy]] and per-[[classes|class]] user's and [[producer-s-accuracy|producer's accuracy]].
- **ES.** Métrica de cuán correctamente una [[classification|clasificación]] o [[estimation|estimación]] coincide con la realidad, típicamente cuantificada como [[overall-accuracy|precisión general]] y [[precision|precisión]] del usuario y productor por clase.

## Understand these first / Entiende esto primero
- [[samples|Samples]] — *data*
    - **EN.** Accuracy is computed by comparing predicted labels to known sample labels.
    - **ES.** La exactitud se calcula comparando las etiquetas predichas con las etiquetas conocidas de las muestras.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]]

## This unlocks / Esto habilita
- [[validation|Validation]] — Validation assesses the accuracy of a classification by comparing its predictions against independent data.
- [[quality|Quality]] — Quality refers to how well data meet requirements for accuracy, precision, and reliability.
- [[performance|Performance]] — Performance measures the accuracy and reliability of a classification or estimation model.
- [[classification-accuracy|Classification accuracy]] — Classification accuracy measures how well a classification map agrees with reference data, extending the concept of accuracy to classification tasks.
- [[higher-classification-accuracy|Higher classification accuracy]] — Higher classification accuracy means a classification method achieves fewer errors than a baseline, often measured by overall accuracy.
- [[model-accuracy|Model accuracy]] — Model accuracy is the accuracy metric applied specifically to a classification model's predictions.
- [[reliable-statistical-analyses|Reliable statistical analyses]] — They incorporate accuracy metrics to correct classification errors and provide valid confidence intervals.
- [[metrics|Metrics]] — Metrics are quantitative measures, such as accuracy, used to evaluate classification performance.
- [[overall-accuracy|Overall accuracy]] — Overall accuracy is the proportion of correctly classified pixels or samples out of the total number.
- [[accuracy-assessment|Accuracy assessment]] — Accuracy assessment quantifies the overall accuracy of a classified map through comparison with reference.
- [[methodological-improvement|Methodological improvement]] — A methodological improvement targets higher accuracy, reducing errors in classification or estimation.
- [[reliability|Reliability]] — Reliability extends accuracy by ensuring results are consistent and dependable over repeated applications.
- [[producer-s-accuracy|Producer's accuracy]] — Producer's accuracy is the probability that a ground truth pixel is correctly classified on the map.
- [[accuracy-metrics|Accuracy metrics]] — Accuracy metrics are specific quantitative measures that evaluate how well a classification matches reality.
- [[confusion-matrix|Confusion matrix]] — Accuracy metrics like overall accuracy are derived from the confusion matrix by comparing predictions to ground truth.
- [[recall|Recall]] — Recall is derived from the confusion matrix as the true positives divided by the sum of true positives and false negatives.
