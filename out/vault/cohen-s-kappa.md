---
id: cohen-s-kappa
kind: concept
category: metric
level: 7
aliases: ["Cohen's Kappa", "Cohen\u2019s Kappa"]
---

# Cohen's Kappa / Kappa de Cohen

> **level 7** · *metric* · sources: cy_colombia · th_validation

**What it is / Qué es.**

- **EN.** A [[statistical|statistical]] [[measure|measure]] of [[inter-rater-agreement|inter-rater agreement]] for categorical items. It quantifies the agreement between two raters (e.g., a [[classified-map|classified map]] and [[reference-datasets|reference data]]) while accounting for the agreement that would occur by chance alone.
- **ES.** Una [[measure|medida]] estadística de [[inter-rater-agreement|acuerdo entre evaluadores]] para elementos categóricos. Cuantifica el acuerdo entre dos evaluadores (por [[example|ejemplo]], un [[classified-map|mapa clasificado]] y [[ground-truth-data|datos de referencia]]) teniendo en cuenta el acuerdo que ocurriría solo por azar.

## Understand these first / Entiende esto primero
- [[confusion-matrix|Confusion matrix]] — *metric*
    - **EN.** Cohen's Kappa quantifies agreement between two raters balancing chance, based on the confusion matrix.
    - **ES.** El Kappa de Cohen cuantifica la concordancia entre dos evaluadores equilibrando el azar, basado en la matriz de confusión.
- [[chance-agreement|Chance agreement]] — *metric*
    - **EN.** Cohen's Kappa corrects observed agreement for chance agreement, giving a reliability measure.
    - **ES.** El Kappa de Cohen corrige el acuerdo observado por el acuerdo por azar, proporcionando una medida de fiabilidad.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[samples|Samples]] → [[accuracy|Accuracy]] → [[validation|Validation]] → [[accuracy-assessment|Accuracy assessment]] → [[confusion-matrix|Confusion matrix]] → [[chance-agreement|Chance agreement]] → [[cohen-s-kappa|Cohen's Kappa]]
