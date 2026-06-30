---
id: multi-task-learning
kind: concept
category: method
level: 4
aliases: ["multi-task learning"]
---

# Multi-task learning / Aprendizaje multitarea

> **level 4** · *method* · sources: uav_field_parcels

**What it is / Qué es.**

- **EN.** A [[machine-learning|machine learning]] [[approach|approach]] where a [[model|model]] is trained simultaneously on multiple related [[tasks|tasks]], sharing representations between tasks to improve generalization and [[performance|performance]], such as jointly learning [[parcels|parcel]] region and boundary [[segmentation|segmentation]].
- **ES.** Un [[approach|enfoque]] de [[machine-learning|aprendizaje automático]] donde un [[model|modelo]] se entrena simultáneamente en múltiples [[tasks|tareas]] relacionadas, compartiendo representaciones entre tareas para mejorar la generalización y el [[yield|rendimiento]], como aprender conjuntamente la [[segmentation|segmentación]] de región y [[boundaries|límites]] de [[parcels|parcelas]].

## Understand these first / Entiende esto primero
- [[machine-learning|Machine learning]] — *method*
    - **EN.** Multi-task learning trains a single model simultaneously on multiple related tasks, improving generalization.
    - **ES.** El aprendizaje multitarea entrena un solo modelo simultáneamente en múltiples tareas relacionadas, mejorando la generalización.
- [[dcp-mtl-model|DCP MTL model]] — *method*
    - **EN.** The DCP MTL model is a multi-task learning model that simultaneously extracts field parcel boundaries and regions from UAV imagery.
    - **ES.** El modelo DCP MTL es un modelo de aprendizaje multitarea que extrae simultáneamente límites de parcelas de campo y regiones a partir de imágenes de UAV.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[training|Training]] → [[machine-learning|Machine learning]] → [[multi-task-learning|Multi-task learning]]
