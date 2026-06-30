# 🧠 Error Analysis: Omission/Commission / Análisis de Errores: Omisión/Comisión

> Cerebro documental — el Handbook es la columna; la investigación es aditiva y citada. / *Documentary brain — Handbook is the backbone; research is additive and cited.*

## English

## Error Analysis: Omission and Commission

Error analysis in remote sensing classification is fundamentally based on two error types derived from the confusion (error) matrix: **omission** and **commission**. Omission errors (false negatives) occur when pixels that truly belong to a class are not classified as such on the map, while commission errors (false positives) occur when pixels are incorrectly assigned to a class [R1]. These errors are calculated from the reference data columns and map rows of the matrix. Omission error is the complement of producer's accuracy (100% - producer's accuracy), and commission error is the complement of user's accuracy (100% - user's accuracy) [R1][R2].

### Key Methods and Distinctions
The confusion matrix summarizes classification accuracy by comparing each map pixel to a reference label. From it, we derive overall accuracy, producer's accuracy, user's accuracy, and the two error types. A critical insight from recent literature is that these class-specific errors are not just descriptive metrics; they are the direct inputs to **bias-corrected area estimation** [R2]. The standard area estimator uses the inverse of the error matrix to adjust for classification bias, allowing accurate area estimation even when map accuracy is modest. This avoids reliance on the kappa coefficient, which has been criticized for its limitations [R2]. Reference data quality itself affects error estimates; errors in ground reference data can propagate and bias area change estimates [R3].

### Grounding Handbook Concepts
- **omission**: A pixel that belongs to a class in reality but is left out of that class on the map. This underestimates the class area.
- **commission**: A pixel assigned to a class on the map that does not belong to it in reality. This overestimates the class area.
- **errors**: Classification mistakes (omission and commission) that cause biased area estimates if uncorrected.
- **overestimation**: Directly linked to commission errors; the predicted area is higher than the actual area.
- **false-positive**: Synonym for commission error, indicating an incorrect assignment to a class.
- **bias**: Systematic deviation from the true value, which can be corrected using the error matrix to obtain unbiased area estimates.

### Gap Filled by Deep Research
The Handbook defines omission and commission but does not fully explain their direct role in area estimation correction. The deep research clarifies that omission and commission are not just accuracy measures but are the building blocks for bias adjustment. It emphasizes that area can be estimated correctly even with moderate map accuracy if the error matrix is properly used [R2]. Moreover, it warns against using kappa and normalized matrices, which obscure these essential error components [R2]. This knowledge is crucial for agricultural statistics, where accurate area estimates are needed for crop monitoring and yield forecasting.

## Español

## Análisis de Errores: Omisión y Comisión

El análisis de errores en la clasificación de teledetección se basa fundamentalmente en dos tipos de error derivados de la matriz de confusión (o de error): **omisión** y **comisión**. Los errores de omisión (falsos negativos) ocurren cuando píxeles que realmente pertenecen a una clase no se clasifican como tal, mientras que los errores de comisión (falsos positivos) ocurren cuando se asignan píxeles incorrectamente a una clase [R1]. Estos errores se calculan a partir de las columnas de referencia y las filas del mapa en la matriz. El error de omisión es el complemento de la exactitud del productor (100% - exactitud del productor), y el error de comisión es el complemento de la exactitud del usuario (100% - exactitud del usuario) [R1][R2].

### Métodos y Distinciones Clave
La matriz de confusión resume la exactitud de la clasificación comparando cada píxel del mapa con una etiqueta de referencia. A partir de ella obtenemos la exactitud global, la exactitud del productor, la exactitud del usuario y los dos tipos de error. Una idea crítica de la literatura reciente es que estos errores específicos por clase no son solo métricas descriptivas; son los insumos directos para la **estimación de área corregida por sesgo** [R2]. El estimador de área estándar usa la inversa de la matriz de error para ajustar por sesgo de clasificación, permitiendo estimar el área correctamente incluso con exactitud del mapa modesta. Esto evita el uso del coeficiente kappa, el cual ha sido criticado por sus limitaciones [R2]. La calidad de los datos de referencia afecta las estimaciones de error; los errores en los datos de referencia pueden propagarse y sesgar las estimaciones de cambio de área [R3].

### Relación con los Conceptos del Manual
- **omisión**: Un píxel que pertenece a una clase en la realidad pero no se clasifica como tal. Subestima el área de la clase.
- **comisión**: Un píxel asignado a una clase en el mapa que no le corresponde en la realidad. Sobreestima el área de la clase.
- **errores**: Equivocaciones de clasificación (omisión y comisión) que causan estimaciones de área sesgadas si no se corrigen.
- **sobreestimación**: Vinculada directamente a errores de comisión; el área predicha es mayor que la real.
- **falso positivo**: Sinónimo de error de comisión, asignación incorrecta a una clase.
- **sesgo**: Desviación sistemática del valor real, que puede corregirse con la matriz de error para obtener estimaciones de área insesgadas.

### Brecha Cubierta por la Investigación Profunda
El Manual define omisión y comisión, pero no explica a fondo su papel directo en la corrección de la estimación de área. La investigación aclara que omisión y comisión no son solo medidas de exactitud, sino los componentes básicos para el ajuste del sesgo. Se enfatiza que el área puede estimarse correctamente incluso con exactitud moderada si se usa adecuadamente la matriz de error [R2]. Además, advierte contra el uso de kappa y matrices normalizadas, que ocultan estos componentes esenciales [R2]. Este conocimiento es crucial para las estadísticas agrícolas, donde se necesitan estimaciones precisas de área para el monitoreo de cultivos y la predicción de rendimientos.

## Referencias verificadas / Verified references
[R1] Accuracy assessment (confusion matrix, omission/commission) - HU Berlin EO Lab — https://eol.pages.cms.hu-berlin.de/geo_rs/S09_Accuracy_assessment.html  *(deep-research)*
[R2] Stehman & Foody, Key issues in rigorous accuracy assessment (RSE 2019) — https://www.sciencedirect.com/science/article/abs/pii/S0034425719302111  *(deep-research)*
[R3] Ground reference data error and mis-estimation of land cover change area (RSL 2013) — https://www.tandfonline.com/doi/full/10.1080/2150704X.2013.798708  *(deep-research)*
[R4] [1] A. Mullissa et al. , “Sentinel-1 SAR Backscatter Analysis Ready Data Preparation in Google Earth Engine ,” Remote Sensing , vol. 13, no. 10, p. 1954, 2021,  — https://doi.org/10.3390/rs13101954  *(handbook-bibliography)*
[R5] [2] C. F. Brown et al. , “Dynamic World , Near real-time global 10 m land use land cover mapping,” Scientific Data , vol. 9, no. 1, p. 251, 2022, doi: 10.1038/s — https://doi.org/10.1038/s41597-022-01307-4  *(handbook-bibliography)*
[R6] [3] D. Amitrano, G. Di Martino, A. Di Simone, and P. Imperatore, “Flood detection with SAR : A review of techniques and datasets,” Remote Sensing , vol. 16, no. — https://doi.org/10.3390/rs16040656  *(handbook-bibliography)*
[R7] [4] B. DeVries, C. Huang, J. Armston, W. Huang, J. W. Jones, and M. W. Lang, “Rapid and robust monitoring of flood events using Sentinel-1 and Landsat data on t — https://doi.org/10.1016/j.rse.2020.111664  *(handbook-bibliography)*
[R8] [9] G. W. Zack, W. E. Rogers, and S. A. Latt, “Automatic measurement of sister chromatid exchange frequency.” Journal of Histochemistry & Cytochemistry , vol. 2 — https://doi.org/10.1177/25.7.70454  *(handbook-bibliography)*
