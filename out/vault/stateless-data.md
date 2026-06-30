---
id: stateless-data
kind: concept
category: data
level: 1
aliases: ["stateless data"]
---

# Stateless data / Datos sin estado

> **level 1** · *data* · sources: howto

**What it is / Qué es.**

- **EN.** [[data|Data]] that is managed without [[persistent-storage|persistent storage]], state, or lifecycle management, as with OCI artifacts mounted as read-only volumes in [[kubernetes|Kubernetes]] sessions, enabling fast startup, automatic caching, and garbage [[collection|collection]] without manual cleanup.
- **ES.** [[data|Datos]] que se gestionan sin [[persistent-storage|almacenamiento persistente]], estado o ciclo de vida, como los artefactos OCI montados como volúmenes de solo lectura en sesiones de [[kubernetes|Kubernetes]], lo que permite un inicio rápido, almacenamiento en caché automático y [[harvest|recolección]] de basura sin limpieza [[handbook|manual]].

## Understand these first / Entiende esto primero
- [[container-image|Container image]] — *primitive*
    - **EN.** Stateless data uses container images for immutable, versioned snapshots of chapter data.
    - **ES.** Los datos sin estado utilizan imágenes de contenedor para instantáneas inmutables y versionadas de los datos del capítulo.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[container-image|Container image]] → [[stateless-data|Stateless data]]

## This unlocks / Esto habilita
- [[oci-artifact|OCI artifact]] — Stateless data is managed as OCI artifacts mounted as read-only volumes, requiring no persistent storage.
