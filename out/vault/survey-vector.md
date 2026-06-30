---
id: survey-vector
kind: concept
category: data
level: 6
aliases: ["survey vector"]
---

# Survey vector / Vector de encuesta

> **level 6** · *data* · sources: crop_statistics_calibration

**What it is / Qué es.**

- **EN.** A [[vector|vector]] representing the [[crop-types|crop type]] observed at a [[pixels|pixel]], with element 1 for the observed [[crop|crop]] and 0 for others. It follows a multinomial [[distribution|distribution]] and is used in [[design|design]]-based [[design-estimator|estimators]] for [[crop-area|crop area]].
- **ES.** Un [[vector|vector]] que representa el [[type|tipo]] de [[crop|cultivo]] observado en un píxel, con el elemento 1 para el cultivo observado y 0 para los demás. Sigue una [[distribution|distribución]] multinomial y se utiliza en estimadores basados en [[design|diseño]] para la [[estimation|estimación]] de áreas.

## Understand these first / Entiende esto primero
- [[survey|Survey]] — *method*
    - **EN.** A survey vector represents the crop type observed at a pixel, with element 1 for the observed crop and 0 for others.
    - **ES.** Un vector de encuesta representa el tipo de cultivo observado en un píxel, con el elemento 1 para el cultivo observado y 0 para los demás.
- [[vector|Vector]] — *data*
    - **EN.** Survey vectors encode ground observations as binary vectors for integration with satellite-derived probability vectors.
    - **ES.** Los vectores de encuesta codifican observaciones de campo como vectores binarios para su integración con vectores de probabilidad derivados de satélite.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[area|Area]] → [[land|Land]] → [[field|Field]] → [[parcels|Parcels]] → [[polygons|Polygons]] → [[vector|Vector]] → [[survey-vector|Survey vector]]
