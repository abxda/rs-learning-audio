---
id: patterns
kind: concept
category: primitive
level: 2
aliases: ["patterns"]
---

# Patterns / Patrones

> **level 2** · *primitive* · sources: ct_chile

**What it is / Qué es.**

- **EN.** Idealized approximations of the [[time-series|time series]] associated with each [[land-cover-classes|land cover class]], derived from [[training-dataset|training data]]. They summarize typical temporal dynamics across [[spectral-bands|spectral bands]] for a given [[classes|class]].
- **ES.** Aproximaciones idealizadas de las series temporales asociadas a cada clase de [[land-cover|cobertura del suelo]], derivadas de [[training-dataset|datos de entrenamiento]]. Resumen las dinámicas temporales típicas en todas las [[bands|bandas espectrales]] para una clase determinada.

## Understand these first / Entiende esto primero
- [[classes|Classes]] — *data*
    - **EN.** For each class, we extract a typical pattern from its training samples to represent the class signature.
    - **ES.** Para cada clase, extraemos un patrón típico de sus muestras de entrenamiento para representar la firma de la clase.
- [[time-series|Time series]] — *data*
    - **EN.** A time series reveals seasonal patterns, which we can generalize into idealized patterns for each land cover class.
    - **ES.** Una serie temporal revela patrones estacionales, que podemos generalizar en patrones idealizados para cada clase de cobertura del suelo.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[images|Images]] → [[time-series|Time series]] → [[patterns|Patterns]]
