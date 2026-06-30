---
id: dcp-mtl-model
kind: concept
category: method
level: 0
aliases: ["DCP MTL model"]
---

# DCP MTL model / modelo DCP MTL

> **level 0** · *method* · sources: uav_field_parcels · uav_field_parcels

**What it is / Qué es.**

- **EN.** A [[multi-task-learning|multi-task learning]] [[model|model]] for extracting [[field|field]] [[parcels|parcel]] [[regions|regions]] and [[boundaries|boundaries]] from [[uav-imagery|UAV imagery]]. It uses a Discrete Cosine Transform module, dual-branch attention, and boundary connectivity modules to achieve precise [[segmentation|segmentation]].
- **ES.** Un [[model|modelo]] de [[multi-task-learning|aprendizaje multitarea]] para extraer [[regions|regiones]] y [[boundaries|límites]] de [[parcels|parcelas]] de [[field|campo]] a partir de [[uav-imagery|imágenes de UAV]]. Utiliza un [[package|módulo]] de Transformada de Coseno Discreta, atención de doble rama y módulos de conectividad de límites para lograr una [[segmentation|segmentación]] precisa.

## This unlocks / Esto habilita
- [[multi-task-learning|Multi-task learning]] — The DCP MTL model is a multi-task learning model that simultaneously extracts field parcel boundaries and regions from UAV imagery.
- [[uav-imagery|UAV imagery]] — It is designed for processing UAV imagery with very high spatial resolution to delineate individual fields.
