---
id: kappa-coefficient
kind: concept
category: metric
level: 6
aliases: ["Kappa Coefficient", "kappa coefficient"]
---

# Kappa Coefficient / Coeficiente Kappa

> **level 6** · *metric* · sources: th_quality_control#validation

**What it is / Qué es.**

- **EN.** The Kappa coefficient is a [[statistical|statistical]] [[measure|measure]] of agreement between [[classified-map|classified map]] and [[reference-datasets|reference data]], accounting for [[chance-agreement|chance agreement]]. [[values|Values]] [[range|range]] from -1 to 1, with higher values indicating better [[accuracy|accuracy]].
- **ES.** El Coeficiente Kappa es una [[measure|medida]] estadística de concordancia entre un [[classified-map|Mapa clasificado]] y [[ground-truth-data|datos de Referencia]], que considera el [[chance-agreement|acuerdo por azar]]. Los [[values|valores]] varían de -1 a 1, donde valores más altos indican mejor [[accuracy|Exactitud]].

## Understand these first / Entiende esto primero
- [[overall-accuracy|Overall accuracy]] — *metric*
    - **EN.** Kappa coefficient goes beyond overall accuracy by accounting for chance agreement in classification.
    - **ES.** El coeficiente Kappa va más allá de la precisión general al considerar el acuerdo por azar en la clasificación.
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** Kappa coefficient measures agreement between classified map and reference data, adjusting for chance agreement.
    - **ES.** El coeficiente Kappa mide la concordancia entre el mapa clasificado y los datos de referencia, ajustando por acuerdo por azar.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[kappa-coefficient|Kappa Coefficient]]
