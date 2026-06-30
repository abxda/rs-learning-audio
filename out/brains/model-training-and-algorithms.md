# 🧠 Model Training and Algorithms / Entrenamiento y Algoritmos de Modelos

> Cerebro documental — el Handbook es la columna; la investigación es aditiva y citada. / *Documentary brain — Handbook is the backbone; research is additive and cited.*

## English

## Overview
Model training and algorithms are the computational core of remote sensing for agricultural statistics. The process transforms labeled training samples into a model that can classify land cover or predict crop yield. The UN Handbook establishes foundational concepts: training fits a machine learning model to labeled data; a model is a trained representation; classification algorithms like Random Forest learn patterns from samples; model training adjusts parameters to minimize error. Deep research adds a modern layer: for satellite image time-series crop classification, Random Forest remains a strong, interpretable baseline, but deep architectures generally improve accuracy. Key methods include 1D temporal CNNs (TempCNN) that use multi-scale temporal filters to better delineate spectrally similar crops than RF [R1]; RNN/LSTM (with attention) that model sequence dynamics; and Transformer (self-attention) architectures that capture temporal and spatial dependencies with strong results [R1]. Benchmarks like BreizhCrops standardize comparison across algorithms [R2]. Interpretability of multi-temporal deep models is an active concern, with efforts to understand what these models learn [R3].

## How It Grounds Handbook Concepts
- **training**: Deep research shows training now involves complex architectures (CNNs, Transformers) that require large labeled datasets and careful hyperparameter tuning [R1].
- **model**: Modern models range from interpretable RF to deep networks; choice depends on accuracy needs and computational resources [R1][R2].
- **classification-algorithm**: Algorithms have evolved from RF to TempCNN, LSTM, and Transformers, each with trade-offs in accuracy and interpretability [R1].
- **model-training**: Training deep models requires more data and computational power; benchmarks like BreizhCrops enable fair comparison [R2].

## Gap Filled
The Handbook provides a general framework but lacks specifics on state-of-the-art algorithms for time-series crop classification. This research fills that gap by detailing deep learning methods (TempCNN, LSTM, Transformers) and their advantages over RF, as well as the importance of benchmarks and interpretability [R1][R2][R3].

## Español

## Resumen
El entrenamiento de modelos y los algoritmos son el núcleo computacional de la teledetección para estadísticas agrícolas. El proceso transforma muestras de entrenamiento etiquetadas en un modelo que puede clasificar la cobertura del suelo o predecir el rendimiento de los cultivos. El Manual de la ONU establece conceptos fundamentales: el entrenamiento ajusta un modelo de aprendizaje automático a datos etiquetados; un modelo es una representación entrenada; los algoritmos de clasificación como Random Forest aprenden patrones de las muestras; el entrenamiento del modelo ajusta parámetros para minimizar errores. La investigación profunda añade una capa moderna: para la clasificación de cultivos en series temporales de imágenes satelitales, Random Forest sigue siendo una línea base sólida e interpretable, pero las arquitecturas profundas generalmente mejoran la precisión. Los métodos clave incluyen CNN temporales 1D (TempCNN) que usan filtros temporales multiescala para delinear mejor cultivos espectralmente similares que RF [R1]; RNN/LSTM (con atención) que modelan dinámicas de secuencia; y arquitecturas Transformer (autoatención) que capturan dependencias temporales y espaciales con resultados sólidos [R1]. Puntos de referencia como BreizhCrops estandarizan la comparación entre algoritmos [R2]. La interpretabilidad de los modelos profundos multitemporales es una preocupación activa, con esfuerzos para entender qué aprenden estos modelos [R3].

## Cómo fundamenta los conceptos del Manual
- **training**: La investigación profunda muestra que el entrenamiento ahora involucra arquitecturas complejas (CNN, Transformers) que requieren grandes conjuntos de datos etiquetados y ajuste cuidadoso de hiperparámetros [R1].
- **model**: Los modelos modernos van desde RF interpretable hasta redes profundas; la elección depende de las necesidades de precisión y recursos computacionales [R1][R2].
- **classification-algorithm**: Los algoritmos han evolucionado de RF a TempCNN, LSTM y Transformers, cada uno con compensaciones en precisión e interpretabilidad [R1].
- **model-training**: Entrenar modelos profundos requiere más datos y poder computacional; puntos de referencia como BreizhCrops permiten una comparación justa [R2].

## Brecha que llena
El Manual proporciona un marco general pero carece de detalles sobre algoritmos de vanguardia para clasificación de cultivos en series temporales. Esta investigación llena esa brecha al detallar métodos de aprendizaje profundo (TempCNN, LSTM, Transformers) y sus ventajas sobre RF, así como la importancia de los puntos de referencia y la interpretabilidad [R1][R2][R3].

## Referencias verificadas / Verified references
[R1] Investigating Temporal CNNs for SITS Classification: a survey (TempCNN) — https://arxiv.org/pdf/2204.08461  *(deep-research)*
[R2] BreizhCrops: A Time Series Dataset for Crop Type Mapping — https://arxiv.org/pdf/1905.11893  *(deep-research)*
[R3] Towards interpreting multi-temporal deep learning models in crop mapping (RSE 2021) — https://www.sciencedirect.com/science/article/abs/pii/S0034425721003199  *(deep-research)*
[R4] [1] I. Becker-Reshef et al. , “Crop type maps for operational global agricultural monitoring,” Scientific Data , vol. 10, no. 1, Mar. 2023, doi: 10.1038/s41597- — https://doi.org/10.1038/s41597-023-02047-9  *(handbook-bibliography)*
[R5] [2] C. Zhang et al. , “Remote sensing for crop mapping: A perspective on current and future crop-specific land cover data products,” Remote Sensing of Environme — https://doi.org/10.1016/j.rse.2025.114995  *(handbook-bibliography)*
[R6] [3] K. Van Tricht et al. , “ESA WorldCereal 10 m 2021 v100.” Zenodo, 2023, doi: 10.5281/ZENODO.7875104 . — https://doi.org/10.5281/ZENODO.7875104  *(handbook-bibliography)*
[R7] [4] C. Butsko et al. , “Deploying geospatial foundation models in the real world: Lessons from WorldCereal.” arXiv, 2025, doi: 10.48550/ARXIV.2508.00858 . — https://doi.org/10.48550/ARXIV.2508.00858  *(handbook-bibliography)*
[R8] [5] S. Karanam et al. , “WorldCereal reference data module (RDM).” International Institute for Applied Systems Analysis (IIASA), 2024, doi: 10.60566/80P50-6Z433 — https://doi.org/10.60566/80P50-6Z433  *(handbook-bibliography)*
