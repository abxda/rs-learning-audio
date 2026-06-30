---
id: oci-artifact
kind: concept
category: phenomenon
level: 2
aliases: ["OCI artifact"]
---

# OCI artifact / artefacto OCI

> **level 2** · *phenomenon* · sources: howto · howto

**What it is / Qué es.**

- **EN.** A versioned, immutable snapshot of a [[chapter|chapter]]'s [[data|data]], packaged as a [[container-image|container image]] and stored in a registry. It is referenced by a [[content-hash|content hash]] (SHA256) for exact [[reproducibility|reproducibility]] and mounted as a read-only volume in a [[kubernetes|Kubernetes]] session.
- **ES.** Una instantánea versionada e inmutable de los [[data|datos]] de un [[chapter|capítulo]], empaquetada como [[container-image|imagen de contenedor]] y almacenada en un registro. Se [[reference|referencia]] mediante un [[content-hash|hash de contenido]] (SHA256) para garantizar la [[reproducibility|reproducibilidad]] exacta y se monta como un volumen de solo lectura en una sesión de [[kubernetes|Kubernetes]].

## Understand these first / Entiende esto primero
- [[stateless-data|Stateless data]] — *data*
    - **EN.** Stateless data is managed as OCI artifacts mounted as read-only volumes, requiring no persistent storage.
    - **ES.** Los datos sin estado se gestionan como artefactos OCI montados como volúmenes de solo lectura, sin requerir almacenamiento persistente.
- [[container-image|Container image]] — *primitive*
    - **EN.** An OCI artifact is a container image packaging chapter-specific data to ensure immutability and reproducibility.
    - **ES.** Un artefacto OCI es una imagen de contenedor que empaqueta datos específicos del capítulo para garantizar inmutabilidad y reproducibilidad.
- [[content-hash|Content hash]] — *primitive*
    - **EN.** OCI artifacts are identified by a content hash, enabling versioned, data integrity verification.
    - **ES.** Los artefactos OCI se identifican mediante un hash de contenido, lo que permite la verificación versionada de la integridad de los datos.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[container-image|Container image]] → [[stateless-data|Stateless data]] → [[oci-artifact|OCI artifact]]
