---
id: cgi-algorithm
kind: concept
category: method
level: 5
aliases: ["CGI algorithm"]
---

# CGI algorithm / algoritmo CGI

> **level 5** · *method* · sources: uav_crop_growth#methods

**What it is / Qué es.**

- **EN.** A [[methods|method]] that monitors [[crop|crop]] [[growth|growth]] by computing multiple [[vegetation-indices|vegetation indices]] from UAV multispectral [[imagery|imagery]], normalizing them, and extracting the first principal [[component|component]] to produce a continuous Crop Growth Index.
- **ES.** Un método que monitorea el [[growth|crecimiento]] de cultivos calculando múltiples [[vegetation-indices|índices de vegetación]] a partir de [[images|imágenes]] multiespectrales de UAV, normalizándolos y extrayendo el primer [[component|componente]] principal para producir un Índice de Crecimiento de Cultivos continuo.

## Understand these first / Entiende esto primero
- [[algorithm|Algorithm]] — *method*
    - **EN.** The CGI algorithm is a defined computational procedure for extracting crop growth indicators from images.
    - **ES.** El algoritmo CGI es un procedimiento computacional definido para extraer indicadores de crecimiento de cultivos a partir de imágenes.
- [[vegetation-indices|Vegetation indices]] — *index*
    - **EN.** By combining multiple vegetation indices, the CGI algorithm captures different aspects of crop growth.
    - **ES.** Al combinar múltiples índices de vegetación, el algoritmo CGI captura diferentes aspectos del crecimiento del cultivo.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[training|Training]] → [[machine-learning|Machine learning]] → [[algorithm|Algorithm]] → [[cgi-algorithm|CGI algorithm]]

## This unlocks / Esto habilita
- [[uav-imagery|UAV imagery]] — The CGI algorithm processes multispectral UAV imagery to compute vegetation indices for crop monitoring.
