---
id: reproducible-code
kind: concept
category: software
level: 5
aliases: ["reproducible code"]
---

# Reproducible code / Código reproducible

> **level 5** · *software* · sources: howto

**What it is / Qué es.**

- **EN.** [[analysis|Analysis]] code (e.g., R, Python scripts) that can be executed by others to produce identical [[results|results]], often packaged in a containerized [[environment|environment]] with all dependencies and [[data|data]].
- **ES.** Código de [[analysis|análisis]] (por [[example|ejemplo]], scripts en R o Python) que otros pueden ejecutar para producir [[results|resultados]] idénticos, a menudo empaquetado en un [[environment|entorno]] contenerizado con todas las dependencias y [[data|datos]].

## Understand these first / Entiende esto primero
- [[reproducible-analysis-system|Reproducible analysis system]] — *method*
    - **EN.** The reproducible analysis system packages the chapter's reproducible code into a pre-configured JupyterLab environment.
    - **ES.** El sistema de análisis reproducible empaqueta el código reproducible del capítulo en un entorno JupyterLab preconfigurado.
- [[workflow|Workflow]] — *method*
    - **EN.** Reproducible code encapsulates the entire workflow from data loading to figure generation in a shareable script.
    - **ES.** El código reproducible encapsula todo el flujo de trabajo, desde la carga de datos hasta la generación de figuras, en un script compartible.
- [[software|Software]] — *primitive*
    - **EN.** Reproducible code packages analysis scripts and dependencies so that others can rerun the same computations.
    - **ES.** El código reproducible empaqueta scripts de análisis y dependencias para que otros puedan reejecutar los mismos cálculos.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[system|System]] → [[methods|Methods]] → [[step|Step]] → [[process|Process]] → [[workflow|Workflow]] → [[reproducible-code|Reproducible code]]

## This unlocks / Esto habilita
- [[reproducibility|Reproducibility]] — Reproducibility in research is achieved by sharing the reproducible code along with data and environment specifications.
- [[jupyter-notebook|Jupyter Notebook]] — Jupyter Notebooks enable reproducible code by combining narrative text with executable code cells.
