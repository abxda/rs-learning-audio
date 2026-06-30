---
id: quality-flags
kind: concept
category: data
level: 2
aliases: ["Quality Flags", "quality flags"]
---

# Quality Flags / Banderas de calidad

> **level 2** · *data* · sources: cy_poland#modis-data

**What it is / Qué es.**

- **EN.** Quality flags are ancillary [[data|data]] [[layers|layers]] in [[satellite|satellite]] products that indicate the [[reliability|reliability]] of each [[pixels|pixel]], such as [[cloud|cloud]] [[cover|cover]], shadow, snow, or [[processing|processing]] [[errors|errors]], used to filter out low-[[quality|quality]] observations.
- **ES.** Las banderas de calidad son [[layers|capas]] de [[data|datos]] auxiliares en productos satelitales que indican la [[reliability|fiabilidad]] de cada píxel, como [[cover|cobertura]] de nubes, sombra, nieve o [[errors|errores]] de [[processing|procesamiento]], utilizadas para filtrar observaciones de baja [[quality|calidad]].

## Understand these first / Entiende esto primero
- [[images|Images]] — *data*
    - **EN.** Satellite images often include quality bands that flag problematic pixels like clouds or shadows.
    - **ES.** Las imágenes satelitales a menudo incluyen bandas de calidad que marcan píxeles problemáticos como nubes o sombras.
- [[pixels|Pixels]] — *data*
    - **EN.** Quality flags are per-pixel indicators of data reliability, such as cloud or shadow presence.
    - **ES.** Las banderas de calidad son indicadores por píxel de la fiabilidad de los datos, como presencia de nubes o sombras.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[images|Images]] → [[pixels|Pixels]] → [[quality-flags|Quality Flags]]

## This unlocks / Esto habilita
- [[quality-band|Quality band]] — Quality bands encode quality flags that indicate cloud, shadow, or sensor conditions per pixel.
