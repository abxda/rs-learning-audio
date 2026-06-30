---
id: pixel-counting
kind: concept
category: method
level: 4
aliases: ["pixel counting"]
---

# Pixel counting / Conteo de píxeles

> **level 4** · *method* · sources: crop_statistics_area

**What it is / Qué es.**

- **EN.** A [[methods|method]] to estimate [[area|area]] by multiplying the [[number|number]] of [[pixels|pixels]] classified as a given [[classes|class]] by the pixel area. It is biased because it integrates classifier [[errors|errors]] and does not correct for [[omission|omission]] or [[commission|commission]].
- **ES.** Un método para estimar [[area|área]] multiplicando el [[number|número]] de [[pixels|píxeles]] clasificados como una clase determinada por el área del píxel. Está sesgado porque integra [[errors|errores]] del clasificador y no corrige omisiones ni comisiones.

## Understand these first / Entiende esto primero
- [[area|Area]] — *metric*
    - **EN.** From a classified map, pixel counting yields the area for each land cover or crop type.
    - **ES.** A partir de un mapa clasificado, el conteo de píxeles produce el área para cada tipo de cobertura del suelo o cultivo.
- [[classified-map|Classified map]] — *product*
    - **EN.** Pixel counting estimates area by multiplying the number of pixels classified as a class by its spatial resolution.
    - **ES.** El conteo de píxeles estima el área multiplicando el número de píxeles clasificados como una clase por su resolución espacial.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[classification|Classification]] → [[classified-map|Classified map]] → [[pixel-counting|Pixel counting]]
