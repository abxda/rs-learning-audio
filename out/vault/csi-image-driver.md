---
id: csi-image-driver
kind: concept
category: software
level: 2
aliases: ["CSI Image Driver"]
---

# CSI Image Driver / Controlador de imágenes CSI

> **level 2** · *software* · sources: howto

**What it is / Qué es.**

- **EN.** A [[kubernetes|Kubernetes]] CSI driver that mounts OCI container [[images|images]] as read-only volumes. It enables fast, [[stateless-data|stateless data]] access by treating [[data|data]] artifacts like compute images, with node-[[level|level]] caching.
- **ES.** Un controlador CSI de [[kubernetes|Kubernetes]] que monta [[images|imágenes]] de contenedor OCI como volúmenes de solo lectura. Permite un acceso rápido y sin estado a los [[data|datos]] al tratar los artefactos de datos como imágenes de computación, con almacenamiento en caché a [[level|nivel]] de nodo.

## Understand these first / Entiende esto primero
- [[data-image|Data image]] — *data*
    - **EN.** The CSI Image Driver mounts OCI container images as read-only volumes for fast, stateless data access.
    - **ES.** El Controlador de imágenes CSI monta imágenes de contenedor OCI como volúmenes de solo lectura para acceso rápido a datos sin estado.
- [[kubernetes|Kubernetes]] — *primitive*
    - **EN.** In a Kubernetes cluster, the CSI Image Driver exposes container images as storage volumes to pods.
    - **ES.** En un clúster de Kubernetes, el CSI Image Driver expone imágenes de contenedor como volúmenes de almacenamiento a los pods.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[data|Data]] → [[data-image|Data image]] → [[csi-image-driver|CSI Image Driver]]
