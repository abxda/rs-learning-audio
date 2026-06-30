---
id: reproducible-analysis-system
kind: concept
category: method
level: 2
aliases: ["reproducible analysis system", "reproducible analysis"]
---

# Reproducible analysis system / Sistema de análisis reproducible

> **level 2** · *method* · sources: howto#reproducible-analysis-system

**What it is / Qué es.**

- **EN.** A [[system|system]] that allows readers to launch a [[chapter|chapter]]'s [[analysis|analysis]] in a one-click, pre-configured [[jupyterlab|JupyterLab]] [[environment|environment]] with all code, [[data|data]], and dependencies ready.
- **ES.** Un [[system|sistema]] que permite a los lectores iniciar el [[analysis|análisis]] de un [[chapter|capítulo]] en un [[jupyterlab|entorno JupyterLab]] preconfigurado con un solo clic, con todo el código, los [[data|datos]] y las dependencias listos.

## Understand these first / Entiende esto primero
- [[chapter|Chapter]] — *primitive*
    - **EN.** Each chapter's analysis is delivered as a self-contained reproducible analysis system with one-click execution.
    - **ES.** El análisis de cada capítulo se entrega como un sistema de análisis reproducible autocontenido con ejecución en un solo clic.
- [[component|Component]] — *primitive*
    - **EN.** A component is a modular software element within the reproducible analysis system that performs a specific task.
    - **ES.** Un componente es un elemento de software modular dentro del sistema de análisis reproducible que realiza una tarea específica.
- [[function|Function]] — *primitive*
    - **EN.** A function in the system is a Dagger SDK unit that encapsulates a single build-time operation.
    - **ES.** Una función en el sistema es una unidad del SDK de Dagger que encapsula una sola operación de tiempo de compilación.

## Lineage to fundamentals / Linaje hasta los fundamentos
[[system|System]] → [[component|Component]] → [[reproducible-analysis-system|Reproducible analysis system]]

## This unlocks / Esto habilita
- [[reproducible-code|Reproducible code]] — The reproducible analysis system packages the chapter's reproducible code into a pre-configured JupyterLab environment.
- [[jupyterlab|JupyterLab]] — JupyterLab provides the interactive web-based interface for launching the reproducible analysis system.
