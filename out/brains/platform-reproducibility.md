# 🧠 Platform & Reproducibility / Plataforma y Reproducibilidad

> Cerebro documental — el Handbook es la columna; la investigación es aditiva y citada. / *Documentary brain — Handbook is the backbone; research is additive and cited.*

## English

## Platform & Reproducibility: The Handbook’s Execution Infrastructure

This theme describes the **reproducible-execution infrastructure** that underpins every chapter of the Handbook. It is not an Earth‑observation method but rather a cloud‑native platform that ensures all code and data can be run identically by any user, anywhere, at any time. The core idea is to decouple data from compute by packaging each chapter’s local data files (models, samples) as immutable, content‑addressed **OCI artifacts** (container images) and mounting them read‑only into Kubernetes pods via a **CSI Image Driver**. This gives fast, stateless, cached startup without requiring persistent storage per session.

### Key Methods & Scientific Distinctions
- **Containerisation (Docker/OCI):** Captures exact software + data versions, enabling cross‑platform reproducibility. This is standard practice in open science (e.g., BinderHub, repo2Docker) and is directly supported by the Handbook’s infrastructure. [R2][R3]
- **Kubernetes CSI Driver:** The Container Storage Interface (CSI) for images allows OCI containers to be mounted as volumes, not run as processes. This is a specialised use of container technology that treats data as read‑only artifacts.
- **Stateless, immutable data:** Each chapter’s data is versioned and hash‑addressed, meaning any change produces a new artifact and the old one remains untouched. This mirrors the reproducibility ideals of data cubes and Earth Observation open science. [R1][R4]

### How It Grounds the Handbook Concepts
- **data-image (data image):** A lightweight OCI container image that holds a chapter’s local data files. It is the unit of data packaging and distribution.
- **data-volumes (DataVolumes):** A Kubernetes resource that imports and persistently stores data from external sources into the cluster; it complements the ephemeral, read‑only data images.
- **csi-image-driver (CSI Image Driver):** A Kubernetes CSI driver that mounts OCI container images as read‑only volumes, enabling fast, stateless data access without running the container as a process.
- **oci-artifact (OCI artifact):** A versioned, immutable snapshot of a chapter’s data, packaged as a container image and registered by content hash. It is the canonical form for all chapter data.

### What Gap It Fills
Before this platform, reproducing a chapter required manually downloading data files, installing dependencies, and hoping the environment matched. The Handbook’s infrastructure fills the gap by providing a **reproducible, automated, and cloud‑native environment** where every user can spin up a session that is bit‑for‑bit identical to the author’s original analysis. This aligns with the broader movement toward reproducible notebooks and application packages in EO science. [R1][R4]

## Español

## Plataforma y Reproducibilidad: Infraestructura de Ejecución del Manual

Este tema describe la **infraestructura de ejecución reproducible** que sustenta cada capítulo del Manual. No es un método de observación de la Tierra, sino una plataforma nativa en la nube que garantiza que todo el código y los datos puedan ejecutarse de manera idéntica por cualquier usuario, en cualquier lugar y en cualquier momento. La idea central es separar los datos del cómputo empaquetando los archivos de datos locales de cada capítulo (modelos, muestras) como **artefactos OCI** inmutables y direccionados por contenido (imágenes de contenedor) y montándolos como solo lectura en pods de Kubernetes mediante un **CSI Image Driver**. Esto proporciona un inicio rápido, sin estado y con caché, sin necesidad de almacenamiento persistente por sesión.

### Métodos Clave y Distinciones Científicas
- **Contenedores (Docker/OCI):** Capturan versiones exactas de software y datos, permitiendo reproducibilidad entre plataformas. Es una práctica estándar en ciencia abierta (ej. BinderHub, repo2Docker) y está directamente soportada por la infraestructura del Manual. [R2][R3]
- **Controlador CSI de Kubernetes:** La interfaz de almacenamiento de contenedores (CSI) para imágenes permite montar contenedores OCI como volúmenes, no ejecutarlos como procesos. Es un uso especializado de la tecnología de contenedores que trata los datos como artefactos de solo lectura.
- **Datos inmutables y sin estado:** Los datos de cada capítulo tienen versiones y se direccionan por hash, de modo que cualquier cambio produce un nuevo artefacto y el anterior permanece intacto. Esto refleja los ideales de reproducibilidad de los cubos de datos y la ciencia abierta de Observación de la Tierra. [R1][R4]

### Cómo Fundamenta los Conceptos del Manual
- **data-image (imagen de datos):** Una imagen de contenedor OCI ligera que contiene los archivos de datos locales de un capítulo. Es la unidad de empaquetado y distribución de datos.
- **data-volumes (volúmenes de datos):** Un recurso de Kubernetes que importa y almacena datos de forma persistente desde fuentes externas al clúster; complementa las imágenes de datos efímeras y de solo lectura.
- **csi-image-driver (controlador de imágenes CSI):** Un controlador CSI de Kubernetes que monta imágenes de contenedor OCI como volúmenes de solo lectura, permitiendo acceso rápido y sin estado a los datos sin ejecutar el contenedor como proceso.
- **oci-artifact (artefacto OCI):** Una instantánea versionada e inmutable de los datos de un capítulo, empaquetada como imagen de contenedor y registrada mediante un hash de contenido. Es la forma canónica de todos los datos del capítulo.

### Qué Vacío Llena
Antes de esta plataforma, reproducir un capítulo requería descargar manualmente los archivos de datos, instalar dependencias y esperar que el entorno coincidiera. La infraestructura del Manual llena el vacío proporcionando un **entorno reproducible, automatizado y nativo en la nube** donde cada usuario puede iniciar una sesión bit‑por‑bit idéntica al análisis original del autor. Esto se alinea con el movimiento hacia cuadernos reproducibles y paquetes de aplicaciones en la ciencia de la Observación de la Tierra. [R1][R4]

## Referencias verificadas / Verified references
[R1] Earth Observation Open Science: Enhancing Reproducible Science Using Data Cubes (Data 2019) — https://www.mdpi.com/2306-5729/4/4/147  *(deep-research)*
[R2] Containers in research workflows: reproducibility (Imperial College carpentry) — https://imperialcollegelondon.github.io/2020-07-13-Containers-Online/08-reproducibility/index.html  *(deep-research)*
[R3] Ten simple rules for writing Dockerfiles for reproducible data science (PLOS Comp Biol 2020) — https://journals.plos.org/ploscompbiol/article?id=10.1371/journal.pcbi.1008316  *(deep-research)*
[R4] OGC Testbed-16: EO Application Packages with Jupyter Notebooks — https://docs.ogc.org/per/20-035.html  *(deep-research)*
