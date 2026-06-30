---
id: data-cube
kind: concept
category: data
level: 5
aliases: ["data cube", "local data cube"]
---

# Data cube / Cubo de datos

> **level 5** · *data* · sources: th_data_cubes#regular-earth-observation-data-cubes

**What it is / Qué es.**

- **EN.** A three-dimensional array of [[satellite-data|satellite data]] with two spatial dimensions and one [[temporal-dimension|temporal dimension]], where each cell has the same spatial [[resolution|resolution]] and regular [[time|time]] intervals, suitable for [[machine-learning|machine learning]].
- **ES.** Un arreglo tridimensional de [[satellite-data|datos satelitales]] con dos dimensiones espaciales y una [[temporal-dimension|dimensión temporal]], donde cada celda tiene la misma [[resolution|resolución]] espacial e intervalos de [[time|tiempo]] regulares, adecuado para [[machine-learning|aprendizaje automático]].

## Understand these first / Entiende esto primero
- [[time|Time]] — *primitive*
    - **EN.** The time dimension in a data-cube allows analysis of temporal changes across repeated satellite observations.
    - **ES.** La dimensión temporal en un cubo de datos permite el análisis de cambios temporales a través de observaciones repetidas de satélite.
- [[satellite-imagery|Satellite imagery]] — *data*
    - **EN.** A data-cube organizes satellite imagery along spatial axes and a time dimension for easy access.
    - **ES.** Un cubo de datos organiza las imágenes satelitales a lo largo de ejes espaciales y una dimensión temporal para facilitar el acceso.
- [[raster|Raster]] — *data*
    - **EN.** A data-cube is a multi-temporal raster where each layer is a spatially aligned image at a different date.
    - **ES.** Un cubo de datos es un ráster multitemporal donde cada capa es una imagen alineada espacialmente en una fecha diferente.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[images|Images]] → [[satellite|Satellite]] → [[remote-sensing|Remote sensing]] → [[sensors|Sensors]] → [[satellite-imagery|Satellite imagery]] → [[data-cube|Data cube]]

## This unlocks / Esto habilita
- [[satellite-data-cube|Satellite data cube]] — A data cube organizes satellite imagery into a regular spatiotemporal array.
- [[brazil-data-cube|Brazil Data Cube]] — The Brazil Data Cube is a cloud service providing open Earth observation data cubes from multiple satellite missions.
