---
id: segmentation
kind: concept
category: method
level: 2
aliases: ["segmentation"]
---

# Segmentation / Segmentación

> **level 2** · *method* · sources: th_parcel_extraction · ct_mexico

**What it is / Qué es.**

- **EN.** The [[process|process]] of partitioning an image into meaningful [[regions|regions]] (segments) that correspond to real-world objects, such as [[agricultural|agricultural]] fields, often as a precursor to [[object-based-classification|object-based classification]].
- **ES.** El [[process|proceso]] de dividir una imagen en [[regions|regiones]] significativas (segmentos) que corresponden a objetos del mundo real, como campos agrícolas, a menudo como precursor de la [[object-based-classification|clasificación basada en objetos]].

## Understand these first / Entiende esto primero
- [[pixels|Pixels]] — *data*
    - **EN.** Segmentation partitions an image into meaningful regions by grouping adjacent pixels with similar properties.
    - **ES.** La segmentación divide una imagen en regiones significativas agrupando píxeles adyacentes con propiedades similares.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[images|Images]] → [[pixels|Pixels]] → [[segmentation|Segmentation]]

## This unlocks / Esto habilita
- [[segmentation-map|Segmentation map]] — A segmentation map stores the output of an image segmentation algorithm, labeling each pixel with a segment ID.
- [[object-based-classification|Object-based classification]] — Object-based classification first segments an image into objects (groups of pixels) and then classifies each object.
- [[boundaries|Boundaries]] — Image segmentation produces boundaries that separate different land cover or crop regions.
