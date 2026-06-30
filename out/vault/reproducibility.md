---
id: reproducibility
kind: concept
category: method
level: 6
aliases: ["reproducibility"]
---

# Reproducibility / Reproducibilidad

> **level 6** · *method* · sources: howto

**What it is / Qué es.**

- **EN.** The ability to obtain identical [[results|results]] from the same [[data|data]] and [[analysis|analysis]] [[methods|methods]], achieved through version control, content-hashed data snapshots, and containerized environments.
- **ES.** Capacidad de obtener [[results|resultados]] idénticos a partir de los mismos [[data|datos]] y [[methods|métodos]] de [[analysis|análisis]], lograda mediante el control de versiones, instantáneas de datos con [[content-hash|hash de contenido]] y entornos contenerizados.

## Understand these first / Entiende esto primero
- [[reproducible-analysis-sessions|Reproducible analysis sessions]] — *method*
    - **EN.** Such sessions ensure reproducibility by encapsulating all software and data needed to re-run an analysis.
    - **ES.** Dichas sesiones garantizan la reproducibilidad al encapsular todo el software y los datos necesarios para volver a ejecutar un análisis.
- [[data-code-availability|Data code availability]] — *primitive*
    - **EN.** Data code availability enables reproducibility by sharing the data and code used in analysis.
    - **ES.** La disponibilidad de datos y código permite la reproducibilidad al compartir los datos y el código utilizados en el análisis.
- [[software|Software]] — *primitive*
    - **EN.** Reproducibility relies on software containers or virtual environments that replicate the exact computational setup.
    - **ES.** La reproducibilidad se basa en contenedores de software o entornos virtuales que replican la configuración computacional exacta.
- [[reproducible-code|Reproducible code]] — *software*
    - **EN.** Reproducibility in research is achieved by sharing the reproducible code along with data and environment specifications.
    - **ES.** La reproducibilidad en la investigación se logra compartiendo el código reproducible junto con los datos y las especificaciones del entorno.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[system|System]] → [[methods|Methods]] → [[step|Step]] → [[process|Process]] → [[workflow|Workflow]] → [[reproducible-code|Reproducible code]] → [[reproducibility|Reproducibility]]
