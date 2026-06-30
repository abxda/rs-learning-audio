---
id: uav-imagery
kind: concept
category: data
level: 6
aliases: ["UAV imagery"]
---

# UAV imagery / imágenes de UAV

> **level 6** · *data* · sources: uav_agriculture_cook_islands

**What it is / Qué es.**

- **EN.** [[images|Images]] captured from Unmanned Aerial Vehicles (drones) at low altitudes, providing very high spatial [[resolution|resolution]] (centimeter-[[level|level]]) for detailed [[agricultural-monitoring|agricultural monitoring]], [[plot|plot]] delineation, and [[crop|crop]] health [[assessment|assessment]].
- **ES.** [[images|Imágenes]] capturadas desde vehículos aéreos no tripulados (drones) a bajas altitudes, que proporcionan una [[resolution|resolución]] espacial muy alta ([[level|nivel]] centimétrico) para el [[agricultural-monitoring|monitoreo agrícola]] detallado, la delimitación de [[parcels|parcelas]] y la [[assessment|evaluación]] de la salud de los cultivos.

## Understand these first / Entiende esto primero
- [[uhr-cfp-dataset|UHR CFP dataset]] — *data*
    - **EN.** The UHR CFP dataset consists of ultra-high resolution imagery from UAVs showing cultivation parcels.
    - **ES.** El conjunto de datos UHR CFP consiste en imágenes de ultra alta resolución de UAV que muestran parcelas de cultivo.
- [[cgi-algorithm|CGI algorithm]] — *method*
    - **EN.** The CGI algorithm processes multispectral UAV imagery to compute vegetation indices for crop monitoring.
    - **ES.** El algoritmo CGI procesa imágenes multiespectrales de UAV para calcular índices de vegetación para el monitoreo de cultivos.
- [[dcp-mtl-model|DCP MTL model]] — *method*
    - **EN.** It is designed for processing UAV imagery with very high spatial resolution to delineate individual fields.
    - **ES.** Está diseñado para procesar imágenes de UAV con muy alta resolución espacial para delimitar campos individuales.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[training|Training]] → [[machine-learning|Machine learning]] → [[algorithm|Algorithm]] → [[cgi-algorithm|CGI algorithm]] → [[uav-imagery|UAV imagery]]

## This unlocks / Esto habilita
- [[drone|Drone]] — Drone imagery provides ultra-high spatial resolution data for detailed crop monitoring.
