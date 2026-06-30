---
id: quality-control
kind: concept
category: method
level: 4
aliases: ["Quality Control", "quality control"]
---

# Quality Control / Control de Calidad

> **level 4** · *method* · sources: th_quality_control#outline

**What it is / Qué es.**

- **EN.** Quality control in [[remote-sensing|remote sensing]] refers to procedures for assessing and improving the [[reliability|reliability]] of [[training-dataset|training data]], classifications, and derived products, including [[detection|detection]] of noisy [[samples|samples]] and [[classes|class]] imbalance correction.
- **ES.** El Control de Calidad en [[remote-sensing|teledetección]] se refiere a procedimientos para evaluar y mejorar la [[reliability|fiabilidad]] de los [[training-dataset|datos de entrenamiento]], clasificaciones y productos derivados, incluyendo la [[detection|detección]] de [[samples|Muestras]] ruidosas y corrección de desbalance de [[classes|Clases]].

## Understand these first / Entiende esto primero
- [[quality|Quality]] — *metric*
    - **EN.** Quality control is a systematic process to ensure data meets required standards through checks and corrections.
    - **ES.** El control de calidad es un proceso sistemático para garantizar que los datos cumplan con los estándares requeridos mediante verificaciones y correcciones.
- [[training-dataset|Training dataset]] — *data*
    - **EN.** Quality control of training data ensures samples are accurate and representative before model training.
    - **ES.** El control de calidad de los datos de entrenamiento asegura que las muestras sean precisas y representativas antes del entrenamiento del modelo.
- [[som-analysis|SOM analysis]] — *method*
    - **EN.** It serves as a quality control step to identify mislabeled samples before training a classifier.
    - **ES.** Sirve como paso de control de calidad para identificar muestras mal etiquetadas antes de entrenar un clasificador.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[quality|Quality]] → [[quality-control|Quality Control]]
