---
id: classified-map
kind: concept
category: product
level: 3
aliases: ["classified CGI map", "classified map", "map product predictions", "satellite map product", "classified maps"]
---

# Classified map / Mapa clasificado

> **level 3** · *product* · sources: th_validation · ct_chile

**What it is / Qué es.**

- **EN.** A [[thematic-map|thematic map]] produced by assigning each [[pixels|pixel]] or object to a [[land-cover|land cover]] or [[crop-types|crop type]] [[classes|class]] using a [[classification-algorithm|classification algorithm]], often validated with [[reference-datasets|reference data]] to assess [[accuracy|accuracy]].
- **ES.** [[thematic-map|Mapa temático]] producido al asignar cada píxel u objeto a una clase de [[land-cover|cobertura del suelo]] o [[type|tipo]] de [[crop|cultivo]] mediante un [[classification-algorithm|algoritmo de clasificación]], a menudo validado con [[ground-truth-data|datos de referencia]] para evaluar la [[accuracy|exactitud]].

## Understand these first / Entiende esto primero
- [[classification|Classification]] — *method*
    - **EN.** A classified map is produced by assigning each pixel or object to a land cover class via classification.
    - **ES.** Un mapa clasificado se produce asignando cada píxel u objeto a una clase de cobertura del suelo mediante clasificación.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[classification|Classification]] → [[classified-map|Classified map]]

## This unlocks / Esto habilita
- [[pixel-counting|Pixel counting]] — Pixel counting estimates area by multiplying the number of pixels classified as a class by its spatial resolution.
