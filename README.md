# Análisis Topológico de Pangea: Búsqueda de los biomas

Este proyecto aplica teoría de grafos y análisis de redes complejas para estudiar
la biogeografía del supercontinente Pangea durante el Triásico (252–201 Ma).
A partir de registros fósiles de la *Paleobiology Database*, se construye una red
de co-ocurrencia entre yacimientos terrestres y se analiza su estructura topológica
para determinar si existían biomas diferenciados a pesar de la continuidad continental.

## INFORMACIÓN EXTRA IMPORTANTE

Este trabajo fue realizado con ayuda de Claude. Aunque la lógica interna y el estudio es 100% nuestro, Claude
nos ha ayudado a crear un trabajo más limpio y profesional. Ha servido como herramienta de apoyo para el estilo 
de los notebooks, la generación de la aplicación web en Streamlit y la creación de gráficos profesionales y
llenos de información. La metodología, el análisis y las conclusiones son trabajo original del equipo.
La decisión de usar IA fue precisamente porque nos ha gustado tanto hacer este trabajo que pensamos que la IA 
nos iba a permitir hacerlo todo de forma más profesional, arreglando nuestros fallos y limpiando nuestras impurezas.

**[Ver la web interactiva](https://trabajo-redespangea.streamlit.app/)**

## Resultados Principales

- **943 yacimientos** conectados por **9.210 aristas** (géneros compartidos).
- Modularidad **Q = 0,72** → biomas claramente diferenciados.
- Red **small-world**: clustering 22× superior al azar con distancia media de 4,09.
- 5 macro-biomas identificados, coherentes con las divisiones paleogeográficas.

## Estructura del Proyecto

- `app.py` — Aplicación web Streamlit (portafolio interactivo).
- `requirements.txt` — Dependencias de la app.
- `src/EDA_01.ipynb` — Pipeline ETL, grafo bipartito, proyección y poda.
- `src/Analisis_Topologico_Pangea.ipynb` — Métricas, modelos nulos, comunidades y sesgo.
- `docs/` — Informe PDF e infografía.
- `red_pangea_interactiva.html` — Visualización interactiva de la red (pyvis).

## Metodología

1. **EDA**: Limpieza de PBDB, filtrado terrestre, extracción de géneros.
2. **Modelado**: Red bipartita (yacimiento–género) → proyección unipartita ponderada.
3. **Poda**: Eliminación de aristas con peso = 1 (géneros cosmopolitas).
4. **Comunidades**: Louvain, Greedy Modularity, Girvan-Newman e InfoMap.
5. **Validación**: Modelos nulos (Erdős-Rényi, Barabási-Albert, Watts-Strogatz) y análisis de sensibilidad.

## Librerías

pandas · numpy · NetworkX · GeoPandas · matplotlib · Plotly · pyvis · Gephi ·
powerlaw · scipy · infomap · Streamlit

## Autores

Raúl Fernández · Aitor Nieto · Juan Carlos Cintas · Javier Riscos
Universidad Politécnica de Madrid · Grado en CDIA · Curso 2025-2026
