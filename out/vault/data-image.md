---
id: data-image
kind: concept
category: data
level: 1
aliases: ["data image"]
---

# Data image / Imagen de datos

> **level 1** · *data* · sources: howto

**What it is / Qué es.**

- **EN.** A lightweight OCI [[container-image|container image]] containing a [[chapter|chapter]]'s local [[data|data]] files (models, [[samples|samples]]), used with a [[csi-image-driver|CSI Image Driver]] for fast, reproducible mounting in [[kubernetes|Kubernetes]] sessions.
- **ES.** [[container-image|Imagen de contenedor]] OCI ligera que contiene los archivos de [[data|datos]] locales de un [[chapter|capítulo]] (modelos, [[samples|muestras]]), utilizada con un [[csi-image-driver|Controlador de imágenes CSI]] para montaje rápido y reproducible en sesiones [[kubernetes|Kubernetes]].

## Understand these first / Entiende esto primero
- [[data|Data]] — *primitive*
    - **EN.** A data image is an OCI container image packaging a chapter's data files for reproducible analysis.
    - **ES.** Una imagen de datos es una imagen de contenedor de OCI que empaqueta los archivos de datos de un capítulo para un análisis reproducible.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[data-image|Data image]]

## This unlocks / Esto habilita
- [[csi-image-driver|CSI Image Driver]] — The CSI Image Driver mounts OCI container images as read-only volumes for fast, stateless data access.
