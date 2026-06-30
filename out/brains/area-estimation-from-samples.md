# 🧠 Area Estimation from Samples / Estimación de Áreas por Muestras

> Cerebro documental — el Handbook es la columna; la investigación es aditiva y citada. / *Documentary brain — Handbook is the backbone; research is additive and cited.*

## English

## Area Estimation from Samples: Design-Based Inference with Map Integration

Area estimation from samples is the gold standard for unbiased quantification of land cover and crop extent. Unlike simple pixel-counting of a thematic map—which is biased due to classification errors that vary by class—design-based inference using a probability sample of reference units produces statistically rigorous estimates with known uncertainty [R1][R2].

The core method is the **error-matrix-adjusted estimator**: a stratified random sample, typically with strata equal to map classes, is collected via ground survey or high-quality reference data. The resulting confusion matrix rescales the map's class proportions by the reference proportions, yielding approximately unbiased area estimates along with standard errors and confidence intervals [R1]. This approach embodies the good-practice triad of sampling, response, and analysis design.

Key methodological points:
- **Stratified random sampling** using the map as a stratification tool greatly increases precision; better maps (higher accuracy) can reduce the required sample size by 20–40% for a target coefficient of variation [R1][R7].
- **Mixed or boundary pixels** introduce proportion estimation bias, addressed by regression, sub-pixel, or unmixing techniques [R6][R3].
- Modern **prediction-powered inference** or **regression estimators** can tighten confidence intervals without introducing bias, especially when auxiliary satellite data are available [R3].

### How This Grounds the Handbook Concepts
- **area-estimation**: Provides the exact statistical framework—error-matrix-adjusted estimator—that converts sample data into unbiased, interpretable area totals for crops or land use.
- **sample-based-estimators**: Specifies the design (stratified by map class) and the estimator (confusion-matrix correction) that are essential for valid area estimation, moving beyond simple pixel counting.
- **ground-survey-estimators**: Refines the notion: ground surveys are not just data collection; they are the reference sample against which map classifications are corrected, producing unbiased estimates.
- **estimator**: Exemplifies a concrete, scientifically validated estimator formulation—with formal variance estimation—that replaces ad-hoc rules.

### GAP Filled
This research fills the critical gap between the Handbook’s conceptual description of area estimation and the operational best practice: it provides the exact statistical recipe (stratified random sampling + confusion-matrix adjustment), explains why pixel counting fails, quantifies the sample-size benefit of better maps, and introduces modern extensions (prediction-powered inference, sub-pixel methods) that are ready for operational use in agricultural statistics. Without this, a user might mistakenly believe a simple map area tally is sufficient, leading to biased statistics [R1][R2][R3].

## Español

## Estimación de Área a Partir de Muestras: Inferencia Basada en Diseño con Integración de Mapas

La estimación de área a partir de muestras es el estándar de oro para cuantificar sin sesgo la extensión de coberturas terrestres y cultivos. A diferencia del simple conteo de píxeles de un mapa temático —que está sesgado debido a errores de clasificación que varían por clase— la inferencia basada en diseño utilizando una muestra probabilística de unidades de referencia produce estimaciones estadísticamente rigurosas con incertidumbre conocida [R1][R2].

El método central es el **estimador ajustado por matriz de error**: se diseña una muestra aleatoria estratificada, típicamente con estratos iguales a las clases del mapa, y se recolectan datos de referencia mediante encuesta de campo o imágenes de alta resolución. La matriz de confusión resultante reescala las proporciones de clase del mapa con las proporciones de referencia, generando estimaciones de área aproximadamente insesgadas junto con errores estándar e intervalos de confianza [R1]. Este enfoque encarna la tríada de buenas prácticas: diseño de muestreo, diseño de respuesta y diseño de análisis.

Puntos metodológicos clave:
- El **muestreo aleatorio estratificado** usando el mapa como herramienta de estratificación aumenta enormemente la precisión; mapas mejores (mayor exactitud) pueden reducir el tamaño de muestra requerido en un 20–40% para un coeficiente de variación objetivo [R1][R7].
- Los **píxeles mixtos o de borde** introducen sesgo en la estimación de proporciones, lo que se aborda mediante técnicas de regresión, subpixel o desmezclado [R6][R3].
- Métodos modernos de **inferencia potenciada por predicción** o **estimadores de regresión** pueden estrechar los intervalos de confianza sin introducir sesgo, especialmente cuando se dispone de datos auxiliares de satélite [R3].

### Cómo Fundamenta los Conceptos del Manual
- **area-estimation**: Proporciona el marco estadístico exacto —estimador ajustado por matriz de error— que convierte datos muestrales en totales de área interpretables y no sesgados para cultivos o usos del suelo.
- **sample-based-estimators**: Especifica el diseño (estratificado por clase del mapa) y el estimador (corrección por matriz de confusión) esenciales para una estimación de área válida, superando el simple conteo de píxeles.
- **ground-survey-estimators**: Refina la noción: las encuestas de campo no son solo recolección de datos; son la muestra de referencia contra la cual se corrigen las clasificaciones del mapa, produciendo estimaciones no sesgadas.
- **estimator**: Ejemplifica una formulación de estimador concreta y científicamente validada —con estimación formal de varianza— que reemplaza reglas ad-hoc.

### Brecha que se Llena
Esta investigación llena la brecha crítica entre la descripción conceptual del Manual sobre estimación de área y la mejor práctica operativa: proporciona la receta estadística exacta (muestreo aleatorio estratificado + ajuste por matriz de confusión), explica por qué el conteo de píxeles falla, cuantifica el beneficio de mapas mejores en el tamaño de muestra, e introduce extensiones modernas (inferencia potenciada por predicción, métodos subpixel) listas para uso operativo en estadísticas agrícolas. Sin esto, un usuario podría creer erróneamente que un simple total de área del mapa es suficiente, llevando a estadísticas sesgadas [R1][R2][R3].

## Referencias verificadas / Verified references
[R1] Olofsson et al., Good practices for estimating area and assessing accuracy of land change (RSE 2014) — https://www.sciencedirect.com/science/article/abs/pii/S0034425714000704  *(deep-research)*
[R2] Gallego, Remote sensing and land cover area estimation (IJRS 2004) — https://doi.org/10.1080/01431160310001619607  *(deep-research)*
[R3] Regression coefficient estimation from remote sensing maps (arXiv 2024) — https://arxiv.org/pdf/2407.13659  *(deep-research)*
[R4] [2] F. D. W. Witmer, “Remote sensing of violent conflict: Eyes from above,” International Journal of Remote Sensing , vol. 36, no. 9, pp. 2326–2352, 2015, doi:  — https://doi.org/10.1080/01431161.2015.1035412  *(handbook-bibliography)*
[R5] [3] X.-P. Song et al. , “National-scale soybean mapping and area estimation in the United States using medium resolution satellite imagery and field survey,” Re — https://doi.org/10.1016/j.rse.2017.01.008  *(handbook-bibliography)*
[R6] [4] R. S. Chhikara, “Effect of mixed (boundary) pixels on crop proportion estimation,” Remote Sensing of Environment , vol. 14, no. 1, pp. 207–218, 1984, doi: 1 — https://doi.org/10.1016/0034-4257(84)90016-6  *(handbook-bibliography)*
[R7] [5] S. Skakun, “The impact of map accuracy on area estimation with remotely sensed data within the stratified random sampling design,” Remote Sensing of Environ — https://doi.org/10.1016/j.rse.2025.114805  *(handbook-bibliography)*
[R8] [6] F. J. Gallego, “Remote sensing and land cover area estimation,” International Journal of Remote Sensing , vol. 25, no. 15, pp. 3019–3047, 2004, doi: 10.1080 — https://doi.org/10.1080/01431160310001619607  *(handbook-bibliography)*
