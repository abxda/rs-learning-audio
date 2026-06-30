---
id: reference-samples
kind: concept
category: data
level: 7
aliases: ["reference samples"]
---

# Reference samples / Muestras de referencia

> **level 7** · *data* · sources: th_quality_control#outline · th_validation#sampling-design

**What it is / Qué es.**

- **EN.** Subset of [[ground-observations|ground observations]] used to train a [[crop-classification-models|classification model]] or validate its output. They must be representative, well-labeled, and independent of the [[model|model]]'s [[training-dataset|training data]] for unbiased [[accuracy-assessment|accuracy assessment]].
- **ES.** Subconjunto de [[ground-observations|observaciones de campo]] utilizado para entrenar un [[model|modelo]] de [[classification|clasificación]] o validar su resultado. Deben ser representativas, estar bien etiquetadas y ser independientes de los [[training-dataset|datos de entrenamiento]] del modelo para una [[accuracy-assessment|evaluación de precisión]] insesgada.

## Understand these first / Entiende esto primero
- [[samples|Samples]] — *data*
    - **EN.** Reference samples are a subset of samples with known ground truth labels used for training or validating models.
    - **ES.** Las muestras de referencia son un subconjunto de muestras con etiquetas de verdad terreno conocidas, utilizadas para entrenar o validar modelos.
- [[ground-truth|Ground-truth]] — *data*
    - **EN.** Reference samples come from ground-truth data and are used to assess classification accuracy.
    - **ES.** Las muestras de referencia provienen de datos de verdad terreno y se utilizan para evaluar la precisión de clasificación.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[classification|Classification]] → [[design|Design]] → [[sampling|Sampling]] → [[survey-approach|Survey approach]] → [[ground-truth|Ground-truth]] → [[reference-samples|Reference samples]]
