---
id: oci-data-artifacts
kind: concept
category: product
level: 1
aliases: ["OCI Data Artifacts"]
---

# OCI Data Artifacts / Artefactos de Datos OCI

> **level 1** · *product* · sources: howto

**What it is / Qué es.**

- **EN.** Immutable, content-hashed snapshots of [[chapter-specific-data|chapter-specific data]] packaged as OCI (Open Container Initiative) [[images|images]]. They are mounted as read-only volumes in [[reproducible-analysis-sessions|reproducible analysis sessions]], ensuring bit-for-bit [[reproducibility|reproducibility]].
- **ES.** Instantáneas inmutables con [[content-hash|hash de contenido]] de [[chapter-specific-data|datos específicos del capítulo]] empaquetadas como [[images|imágenes]] OCI (Open Container Initiative). Se montan como volúmenes de solo lectura en [[reproducible-analysis-sessions|sesiones de análisis reproducibles]], garantizando la [[reproducibility|reproducibilidad]] bit a bit.

## Understand these first / Entiende esto primero
- [[data|Data]] — *primitive*
    - **EN.** OCI data artifacts are immutable, content-hashed snapshots of chapter-specific data packaged as OCI container images.
    - **ES.** Los artefactos de datos OCI son instantáneas inmutables con hash de contenido de datos específicos del capítulo empaquetadas como imágenes de contenedor OCI.
- [[reproducible-analysis-sessions|Reproducible analysis sessions]] — *method*
    - **EN.** OCI data artifacts enable reproducible analysis sessions by providing versioned, self-contained data that can be mounted in JupyterLab environments.
    - **ES.** Los artefactos de datos OCI permiten sesiones de análisis reproducibles al proporcionar datos versionados y autocontenidos que se pueden montar en entornos JupyterLab.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[oci-data-artifacts|OCI Data Artifacts]]
