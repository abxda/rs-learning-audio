---
id: image-segmentation
kind: concept
category: method
level: 2
aliases: ["image segmentation"]
---

# Image segmentation / Segmentación de imágenes

> **level 2** · *method* · sources: th_parcel_extraction

**What it is / Qué es.**

- **EN.** The [[process|process]] of partitioning an image into multiple segments (sets of [[pixels|pixels]]), often used to delineate objects like [[agricultural|agricultural]] [[field|field]] [[parcels|parcels]] by grouping spectrally similar pixels into homogeneous [[regions|regions]].
- **ES.** [[process|Proceso]] de dividir una imagen en múltiples segmentos (conjuntos de [[pixels|píxeles]]), a menudo utilizado para delinear objetos como [[agricultural-plots|parcelas agrícolas]] agrupando píxeles espectralmente similares en [[regions|regiones]] homogéneas.

## Understand these first / Entiende esto primero
- [[pixels|Pixels]] — *data*
    - **EN.** Image segmentation partitions an image into meaningful groups of adjacent pixels (segments).
    - **ES.** La segmentación de imágenes divide una imagen en grupos significativos de píxeles adyacentes (segmentos).
- [[segment-model|Segment Model]] — *method*
    - **EN.** It is designed specifically for the task of image segmentation, often using architectures like SAM.
    - **ES.** Está diseñado específicamente para la tarea de segmentación de imágenes, a menudo utilizando arquitecturas como SAM.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[images|Images]] → [[pixels|Pixels]] → [[image-segmentation|Image segmentation]]

## This unlocks / Esto habilita
- [[sam|SAM]] — SAM (Segment Anything Model) is a deep learning model that performs image segmentation from prompts.
- [[segment|Segment]] — A segment is a group of contiguous pixels produced by image segmentation, representing a homogeneous area.
