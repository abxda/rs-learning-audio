# 🧠 Geospatial Data Handling / Manejo de Datos Geoespaciales

> Cerebro documental — el Handbook es la columna; la investigación es aditiva y citada. / *Documentary brain — Handbook is the backbone; research is additive and cited.*

## English

## Geospatial Data Handling: The Foundation of Remote Sensing for Agricultural Statistics

Effective agricultural statistics from remote sensing depend on precise geospatial data handling. The core challenge is linking Earth observation data (satellite images) with survey data (field observations). This requires a Coordinate Reference System (CRS) to give coordinates geographic meaning, ensuring data layers align correctly [R1]. Map projections transform the 3D Earth to a 2D plane, each trading off area, shape, or distance [R3]. Data are structured as **vector** (points, lines, polygons for discrete features like field boundaries) or **raster** (grid cells for continuous variables like NDVI). Reprojecting vector data moves vertices; reprojecting raster resamples values to a new grid, affecting pixel alignment and accuracy [R2]. The **gap** the Handbook leaves is the explicit mechanical difference between vector and raster reprojection and the practical importance of choosing the correct CRS when integrating multiple data sources, such as combining satellite imagery (often in a geographic CRS like WGS84) with survey GPS points (collected in a projected CRS).

### How it grounds Handbook concepts:
- **georeferenced-information**: A CRS is the mechanism that transforms raw coordinates into georeferenced information, enabling spatial analysis [R1].
- **geospatial-data**: The vector/raster distinction is fundamental; both require correct CRS handling to be useful geospatial data [R3].
- **spatial-information**: Accurate location and shape (spatial information) rely on proper reprojection to preserve geometry [R2].
- **geographic-data**: Geographic data integrity depends on consistent CRS use to avoid misalignment errors [R1].
- **geoinformation**: Geoinformation becomes actionable when coordinate systems ensure reliable spatial relationships [R3].
- **gis**: GIS software tools manage CRS definitions, reprojections, and overlays for integrated analysis [R2].

## Español

## Manejo de Datos Geoespaciales: La Base para Estadísticas Agrícolas con Teledetección

Las estadísticas agrícolas confiables a partir de teledetección dependen de un manejo preciso de datos geoespaciales. El desafío central es vincular datos de observación de la Tierra (imágenes satelitales) con datos de encuestas (observaciones de campo). Esto requiere un Sistema de Referencia de Coordenadas (SRC) que otorgue significado geográfico a las coordenadas, asegurando que las capas de datos se alineen correctamente [R1]. Las proyecciones cartográficas transforman la Tierra 3D a un plano 2D, cada una compensando área, forma o distancia [R3]. Los datos se estructuran como **vectoriales** (puntos, líneas, polígonos para entidades discretas como límites de parcelas) o **ráster** (celdas de cuadrícula para variables continuas como NDVI). Reprojectar datos vectoriales mueve vértices; reprojectar ráster remuestrea valores a una nueva cuadrícula, afectando la alineación de píxeles y la precisión [R2]. La **brecha** que deja el Manual es la diferencia mecánica explícita entre reproyección vectorial y ráster, y la importancia práctica de elegir el SRC correcto al integrar múltiples fuentes de datos, como combinar imágenes satelitales (a menudo en un SRC geográfico como WGS84) con puntos GPS de encuestas (recopilados en un SRC proyectado).

### Cómo fundamenta los conceptos del Manual:
- **georeferenced-information**: Un SRC es el mecanismo que transforma coordenadas brutas en información georreferenciada, habilitando el análisis espacial [R1].
- **geospatial-data**: La distinción vectorial/ráster es fundamental; ambos requieren un manejo correcto del SRC para ser datos geoespaciales útiles [R3].
- **spatial-information**: La ubicación y forma precisas (información espacial) dependen de una reproyección adecuada para preservar la geometría [R2].
- **geographic-data**: La integridad de los datos geográficos depende del uso consistente del SRC para evitar errores de desalineación [R1].
- **geoinformation**: La geoinformación se vuelve procesable cuando los sistemas de coordenadas aseguran relaciones espaciales confiables [R3].
- **gis**: Las herramientas de software GIS gestionan definiciones de SRC, reproyecciones y superposiciones para un análisis integrado [R2].

## Referencias verificadas / Verified references
[R1] Introduction to Coordinate Reference Systems (UW-Madison Data Science) — https://uw-madison-datascience.github.io/organization-geospatial/03-crs/index.html  *(deep-research)*
[R2] Reprojecting geographic data (Geocomputation with R, ch.7) — https://r.geocompx.org/reproj-geo-data  *(deep-research)*
[R3] Coordinate Reference Systems (QGIS gentle GIS introduction) — https://docs.qgis.org/3.44/en/docs/gentle_gis_introduction/coordinate_reference_systems.html  *(deep-research)*
[R4] [6] P. Sarricolea, M. Herrera-Ossandon, and Ó. Meseguer-Ruiz, “Climatic regionalisation of continental Chile,” Journal of Maps , vol. 13, no. 2, pp. 66–73, Nov. — https://doi.org/10.1080/17445647.2016.1259592  *(handbook-bibliography)*
[R5] [10] H. E. Beck, N. E. Zimmermann, T. R. McVicar, N. Vergopolan, A. Berg, and E. F. Wood, “Present and future Köppen-Geiger climate classification maps at 1-km  — https://doi.org/10.1038/sdata.2018.214  *(handbook-bibliography)*
[R6] [11] G. O. Ojwang et al. , “An integrated hierarchical classification and machine learning approach for mapping land use and land cover in complex social-ecolog — https://doi.org/10.3389/frsen.2023.1188635  *(handbook-bibliography)*
[R7] [12] Md. S. Chowdhury, “GIS based method for mapping actual LULC by combining seasonal LULCs,” MethodsX , vol. 11, p. 102472, Dec. 2023, doi: 10.1016/j.mex.2023 — https://doi.org/10.1016/j.mex.2023.102472  *(handbook-bibliography)*
[R8] [13] D. T. Myers, D. Jones, D. Oviedo-Vargas, J. P. Schmit, D. L. Ficklin, and X. Zhang, “Seasonal variation in land cover estimates reveals sensitivities and o — https://doi.org/10.5194/hess-28-5295-2024  *(handbook-bibliography)*
