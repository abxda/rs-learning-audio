# 🧠 Image Preprocessing Basics / Fundamentos de Preprocesamiento

> Cerebro documental — el Handbook es la columna; la investigación es aditiva y citada. / *Documentary brain — Handbook is the backbone; research is additive and cited.*

## English

# Image Preprocessing Basics

Image preprocessing transforms raw satellite data into analysis-ready products. It encompasses geometric, radiometric, and atmospheric corrections, as well as cloud masking and temporal compositing. These steps are essential for producing consistent surface reflectance measurements used in agricultural statistics.

## Key Methods and Distinctions

**Radiometric calibration** converts raw digital numbers (DN) to physical radiance or reflectance, correcting sensor noise and striping. **Atmospheric correction** removes scattering and absorption effects from the atmosphere to obtain Bottom-of-Atmosphere (BOA) reflectance. For Sentinel-2, Level-1C provides Top-of-Atmosphere (TOA) reflectance with geometric and orthorectification corrections, while Level-2A (produced by SEN2COR) applies atmospheric, cirrus and terrain correction to yield BOA reflectance [R1][R3]. The Harmonized Landsat Sentinel-2 (HLS) dataset offers cross-sensor Analysis Ready Data (ARD) surface reflectance, facilitating multi-temporal analysis [R2].

**Geometric correction** aligns imagery to map coordinates, essential for multi-temporal and multi-sensor integration. **Terrain correction** is especially critical for SAR imagery, correcting foreshortening, layover, and shadow distortions using digital elevation models. **Cloud masking** identifies and removes cloudy pixels using spectral tests (e.g., Sentinel-2 scene classification). Temporal compositing reduces residual cloud contamination and provides gap-free datasets for crop monitoring.

## Grounding Handbook Concepts

- **processing**: The Handbook defines processing as steps applied to raw data for analysis. This includes both geometric and radiometric corrections, as expanded by deep research into atmospheric correction and cloud masking.
- **data-processing**: The conversion of raw satellite data into usable information is realized through the preprocessing pipeline: from raw DN to calibrated TOA, then atmospherically corrected BOA, followed by cloud masking and compositing to produce analysis-ready mosaics.
- **atmospheric-correction**: The Handbook describes removal of atmospheric effects. Deep research specifies that Sentinel-2 Level-2A (SEN2COR) performs this correction, including AOT and water vapour retrieval, enabling consistent surface reflectance for classification [R1][R3].
- **terrain-correction**: The Handbook mentions SAR geometric distortions. Research confirms that digital elevation models are used to correct foreshortening, layover and shadow, and that SEN2COR also includes terrain correction for optical data.

## Gap Filled by Deep Research

The deep research provides concrete examples (Sentinel-2 processing levels, SEN2COR, HLS) and quantifies the impact of atmospheric correction on land-cover classification accuracy [R1]. It links preprocessing to Analysis Ready Data concepts and cross-sensor harmonization [R2], filling the gap between generic Handbook definitions and practical implementation in modern Earth observation systems.

## Español

# Fundamentos de Preprocesamiento de Imágenes

El preprocesamiento transforma datos satelitales crudos en productos listos para análisis. Incluye correcciones geométricas, radiométricas y atmosféricas, más enmascaramiento de nubes y composición temporal. Estos pasos son esenciales para obtener reflectancia superficial consistente para estadísticas agrícolas.

## Métodos Clave y Distinciones

**La calibración radiométrica** convierte números digitales (DN) en radiancia/reflectancia física, corrigiendo ruido del sensor. **La corrección atmosférica** elimina efectos de dispersión/absorción para obtener reflectancia de fondo de atmósfera (BOA). Para Sentinel-2, el nivel 1C proporciona reflectancia TOA con corrección geométrica/ortorrectificación; el nivel 2A (SEN2COR) aplica corrección atmosférica, de cirros y terreno para obtener BOA [R1][R3]. El conjunto de datos Harmonized Landsat Sentinel-2 (HLS) ofrece reflectancia superficial ARD entre sensores [R2].

**La corrección geométrica** alinea imágenes a coordenadas de mapa, esencial para análisis multitemporal. **La corrección de terreno** es crítica en SAR, corrigiendo acortamiento, layover y sombra mediante modelos de elevación digital. **El enmascaramiento de nubes** identifica píxeles nublados con pruebas espectrales. La composición temporal reduce contaminación residual.

## Conceptos del Manual

- **processing**: El Manual define procesamiento como pasos para análisis. La investigación añade corrección atmosférica y enmascaramiento.
- **data-processing**: La conversión de datos crudos a información útil: DN → TOA calibrado → BOA → enmascarado → compuesto.
- **atmospheric-correction**: El Manual describe eliminación de efectos atmosféricos. Investigación especifica que Level-2A (SEN2COR) produce reflectancia superficial [R1][R3].
- **terrain-correction**: El Manual menciona distorsiones geométricas SAR. Investigación confirma uso de DEM y que SEN2COR incluye corrección de terreno para óptico.

## Brecha Cubierta

La investigación proporciona ejemplos concretos (niveles Sentinel-2, SEN2COR, HLS) y cuantifica el impacto de la corrección atmosférica en clasificación [R1], vinculando preprocesamiento con ARD y armonización entre sensores [R2].

## Referencias verificadas / Verified references
[R1] Impact of Atmospheric Corrections on Sentinel-2 Land-Cover Classification (MDPI IJGI 2020) — https://www.mdpi.com/2220-9964/9/4/277  *(deep-research)*
[R2] Harmonized Landsat and Sentinel-2 v2.0 surface reflectance dataset (RSE 2025) — https://www.sciencedirect.com/science/article/pii/S0034425725001270  *(deep-research)*
[R3] Assessment of atmospheric correction methods for Sentinel-2 (ISPRS/IJAEOG) — https://www.sciencedirect.com/science/article/abs/pii/S0303243418301843  *(deep-research)*
[R4] [1] L. Ambrosio, L. Iglesias, C. Marín, and N. Deffense, “Integration of remote sensing data into national statistical office sampling designs for agriculture,” — https://doi.org/10.3233/SJI-220116  *(handbook-bibliography)*
[R5] [3] P. Olofsson, G. M. Foody, M. Herold, S. V. Stehman, C. E. Woodcock, and M. A. Wulder, “Good practices for estimating area and assessing accuracy of land cha — https://doi.org/10.1016/j.rse.2014.02.015  *(handbook-bibliography)*
[R6] [4] R. E. McRoberts et al. , “On the model-assisted regression estimators using remotely sensed auxiliary data,” Remote Sensing of Environment , vol. 281, p. 11 — https://doi.org/10.1016/j.rse.2022.113168  *(handbook-bibliography)*
[R7] [5] A. N. Angelopoulos, S. Bates, C. Fannjiang, M. I. Jordan, and T. Zrnic, “Prediction-powered inference,” Science , vol. 382, no. 6671, pp. 669–674, 2023, doi — https://doi.org/10.1126/science.adi6000  *(handbook-bibliography)*
[R8] [7] K. Lu, D. M. Kluger, S. Bates, and S. Wang, “Regression coefficient estimation from remote sensing maps,” Remote Sensing of Environment , vol. 330, p. 11494 — https://doi.org/10.1016/j.rse.2025.114949  *(handbook-bibliography)*
