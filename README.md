# Análisis Topológico de Pangea mediante Redes Bipartitas Fósiles

Este proyecto aplica teoría de grafos y análisis de redes complejas para reconstruir matemáticamente el supercontinente Pangea durante el periodo Triásico. 

A través de la extracción de registros de la *Paleobiology Database*, se proyecta una red bipartita (Yacimiento-Fósil) para analizar la conectividad paleobiogeográfica mediante métricas de centralidad y detección de comunidades.

## Estructura del Proyecto
* `data/`: Contiene los datasets en crudo extraídos (ignorados en el repositorio por tamaño).
* `src/`: Scripts modulares en Python (`.py`) para las tareas de ETL y modelado del grafo.
* `notebooks/`: Cuadernos interactivos Jupyter para la visualización y redacción del informe final científico.

## Metodología y Algoritmos
1. **Modelado**: Proyección unipartita usando el Índice de Similitud de Jaccard.
2. **Comunidades**: Algoritmo de Louvain para la identificación de paleobiomas.
3. **Métricas**: *Betweenness Centrality* para identificar corredores biológicos clave.

## Tecnologías Utilizadas
* `pandas` y `numpy` para limpieza y Feature Engineering.
* `networkx` para la topología matemática.
* `matplotlib` para visualización de red.
