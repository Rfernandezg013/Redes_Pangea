"""
╔══════════════════════════════════════════════════════════════════════════════╗
║  ANÁLISIS TOPOLÓGICO DE PANGEA: Biogeografía de Co-ocurrencia Fósil       ║
║  Portafolio interactivo — Streamlit App                                     ║
║                                                                              ║
║  Grado en Ciencia de Datos e Inteligencia Artificial                        ║
║  Universidad Politécnica de Madrid · Computación Social y Personalización   ║
║  Curso 2025-2026                                                             ║
╚══════════════════════════════════════════════════════════════════════════════╝

INSTRUCCIONES DE USO:
    1. Instalar dependencias:
       pip install streamlit pandas plotly
    2. Ejecutar:
       streamlit run app.py
    3. Archivos opcionales (colocar en la misma carpeta que app.py):
       - infografia.png                → Captura de la infografía del proyecto
       - red_pangea_interactiva.html   → HTML generado por pyvis (notebook EDA_01)
"""

import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import os

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURACIÓN GLOBAL DE LA PÁGINA
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Análisis Topológico de Pangea",
    page_icon="🦕",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ─────────────────────────────────────────────────────────────────────────────
# ESTILOS CSS — Tema oscuro inspirado en la infografía
# Se usa .stMarkdown para no romper iconos internos de Streamlit
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=Source+Sans+3:wght@300;400;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

.stApp {
    background: linear-gradient(175deg, #060d1a 0%, #0a1628 40%, #0d1f35 100%);
    color: #c8d6e5;
}

div[data-testid="stMetric"] {
    background: linear-gradient(135deg, rgba(42,157,143,0.12) 0%, rgba(0,48,73,0.2) 100%);
    border: 1px solid rgba(42,157,143,0.25);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.3);
}
div[data-testid="stMetric"] label {
    color: #5eead4 !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}
div[data-testid="stMetric"] div[data-testid="stMetricValue"] {
    color: #f0f9ff !important;
    font-family: 'Playfair Display', serif !important;
    font-weight: 900 !important;
    font-size: 2rem !important;
}
div[data-testid="stMetric"] div[data-testid="stMetricDelta"] {
    color: #94a3b8 !important;
    font-family: 'Source Sans 3', sans-serif !important;
}

h1 {
    font-family: 'Playfair Display', serif !important;
    color: #f0f9ff !important;
    font-weight: 900 !important;
    letter-spacing: -0.5px;
}
h2 {
    font-family: 'Playfair Display', serif !important;
    color: #5eead4 !important;
    font-weight: 700 !important;
    border-bottom: 2px solid rgba(42,157,143,0.3);
    padding-bottom: 8px;
    margin-top: 2.5rem !important;
}
h3 {
    font-family: 'Source Sans 3', sans-serif !important;
    color: #7dd3fc !important;
    font-weight: 600 !important;
}

/* Solo textos de markdown, NO iconos ni spans internos de Streamlit */
.stMarkdown p,
.stMarkdown li {
    font-family: 'Source Sans 3', sans-serif !important;
    line-height: 1.75;
}

table { border-collapse: collapse; width: 100%; }
th {
    background: rgba(42,157,143,0.18) !important;
    color: #5eead4 !important;
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 700 !important;
    padding: 10px 14px !important;
    text-align: left;
    border-bottom: 2px solid rgba(42,157,143,0.4);
}
td {
    padding: 8px 14px !important;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    color: #c8d6e5 !important;
    font-family: 'Source Sans 3', sans-serif !important;
}

code {
    font-family: 'JetBrains Mono', monospace !important;
    background: rgba(0,48,73,0.5) !important;
    color: #7dd3fc !important;
    border-radius: 4px;
    padding: 2px 6px;
}

details {
    background: rgba(0,48,73,0.2) !important;
    border: 1px solid rgba(42,157,143,0.15) !important;
    border-radius: 10px !important;
}

hr {
    border-color: rgba(42,157,143,0.2) !important;
    margin: 2rem 0;
}

button[data-baseweb="tab"] {
    font-family: 'Source Sans 3', sans-serif !important;
    font-weight: 600 !important;
    color: #94a3b8 !important;
}
button[data-baseweb="tab"][aria-selected="true"] {
    color: #5eead4 !important;
    border-bottom-color: #2a9d8f !important;
}

section[data-testid="stSidebar"] {
    background: #060d1a !important;
    border-right: 1px solid rgba(42,157,143,0.15);
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}

div[data-testid="stAlert"] {
    background: rgba(0,48,73,0.25) !important;
    border: 1px solid rgba(42,157,143,0.2) !important;
    border-radius: 10px !important;
}

blockquote {
    border-left: 3px solid #2a9d8f !important;
    padding-left: 1rem;
    color: #94a3b8 !important;
    font-style: italic;
}

/* ── Pipeline ETL boxes ── */
.pipeline-container {
    display: flex;
    align-items: flex-start;
    justify-content: center;
    gap: 6px;
    padding: 20px 10px;
    flex-wrap: nowrap;
}
.pipeline-step {
    flex: 1 1 0;
    min-width: 130px;
    max-width: 180px;
    background: rgba(42,157,143,0.08);
    border: 1.5px solid #2a9d8f;
    border-radius: 10px;
    padding: 14px 10px 16px;
    text-align: center;
}
.pipeline-num {
    background: #2a9d8f;
    color: #0a1628;
    font-family: 'Source Sans 3', sans-serif;
    font-weight: 700;
    font-size: 0.8rem;
    width: 28px; height: 28px;
    line-height: 28px;
    border-radius: 50%;
    margin: 0 auto 8px;
}
.pipeline-title {
    color: #5eead4;
    font-family: 'Source Sans 3', sans-serif;
    font-weight: 700;
    font-size: 0.9rem;
    margin-bottom: 8px;
}
.pipeline-desc {
    color: #94a3b8;
    font-family: 'Source Sans 3', sans-serif;
    font-size: 0.75rem;
    line-height: 1.5;
    text-align: center;
}
.pipeline-arrow {
    flex: 0 0 24px;
    display: flex;
    align-items: center;
    justify-content: center;
    color: #2a9d8f;
    font-size: 1.4rem;
    padding-top: 45px;
}
</style>
""", unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 · HEADER / HERO
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("""
<div style="text-align:center; padding: 8px 0 0 0;">
    <span style="font-family:'JetBrains Mono',monospace; font-size:0.75rem;
    color:#2a9d8f; letter-spacing:4px; text-transform:uppercase;">
    Universidad Politécnica de Madrid · Grado en CDIA · Computación Social y Personalización
    </span>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div style="text-align:center; padding: 20px 0 5px 0;">
    <h1 style="font-size:3rem; margin-bottom:0; line-height:1.15;
    background: linear-gradient(135deg, #f0f9ff 0%, #5eead4 50%, #2a9d8f 100%);
    -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
        Análisis Topológico de Pangea
    </h1>
    <p style="font-family:'Playfair Display',serif; font-size:1.35rem;
    color:#7dd3fc; margin-top:4px; font-weight:400; font-style:italic;">
        Biogeografía de Co-ocurrencia Fósil en el Triásico (252–201 Ma)
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<p style="text-align:center; color:#64748b; font-size:0.9rem; margin-top:0;">
    Raúl Fernández · Aitor Nieto · Juan Carlos Cintas · Javier Riscos
    &nbsp;|&nbsp; Curso 2025-2026
</p>
""", unsafe_allow_html=True)

st.markdown("---")

st.markdown("""
> Este trabajo presenta un análisis de redes complejas aplicado a la biogeografía del Triásico.
> A partir de los registros fósiles de la **Paleobiology Database (PBDB)**, se construye una red
> de co-ocurrencia entre yacimientos terrestres de Pangea, donde dos yacimientos se conectan
> si comparten géneros fósiles. La red resultante se analiza topológicamente y se somete a
> detección de comunidades mediante el algoritmo de **Louvain**, obteniendo una modularidad
> que confirma la existencia de **macro-biomas diferenciados** en el supercontinente.
""")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Nodos (Yacimientos)", "943", delta="Terrestres del Triásico")
col2.metric("Aristas (Conexiones)", "9.210", delta="Géneros compartidos")
col3.metric("Modularidad Q", "0.72", delta="Fuerte estructura modular")
col4.metric("Grado Medio ⟨k⟩", "19.5", delta="Conexiones por yacimiento")

# ┌────────────────────────────────────────────────────────────────────┐
# │ Coloca tu infografía como 'infografia.png' junto a app.py        │
# └────────────────────────────────────────────────────────────────────┘
RUTA_INFOGRAFIA = "extras/infografia.png"
if os.path.exists(RUTA_INFOGRAFIA):
    st.image(RUTA_INFOGRAFIA, use_container_width=True,
             caption="Infografía resumen del proyecto")


# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 · CONTEXTO PALEOBIOLÓGICO
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("## Contexto Paleobiológico")

ctx_col1, ctx_col2 = st.columns([3, 2])

with ctx_col1:
    st.markdown("""
    Durante el período **Triásico (252–201 Ma)**, la totalidad de las masas continentales
    estaban unidas en el supercontinente **Pangea**. Esta configuración geográfica única
    plantea una pregunta fundamental para la paleobiogeografía:
    """)
    st.markdown("""
    <div style="background: rgba(42,157,143,0.08); border-left:4px solid #2a9d8f;
    padding:16px 20px; border-radius:0 8px 8px 0; margin: 16px 0; font-size:1.1rem;">
        <strong>Si todos los continentes estaban conectados físicamente, ¿existían biomas
        diferenciados o la fauna se distribuía de forma homogénea?</strong>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("""
    Para responder a esta cuestión se aplican técnicas de **análisis de redes complejas**
    sobre datos del registro fósil. Se modela la relación entre yacimientos paleontológicos
    como una **red de co-ocurrencia ponderada**, donde el peso de cada conexión refleja el
    número de géneros fósiles compartidos. La detección de comunidades sobre esta red
    permite identificar agrupaciones de yacimientos con faunas similares, interpretables
    como **macro-biomas del Triásico**.
    """)

with ctx_col2:
    st.markdown("""
    ### Enfoque Metodológico

    Este proyecto combina tres disciplinas:

    - **Ingeniería de Datos** — Pipeline ETL sobre la PBDB, la mayor base de datos
      abierta de ocurrencias fósiles del mundo.
    - **Teoría de Redes Complejas** — Métricas topológicas, modelos nulos y propiedades
      de mundo pequeño (*small-world*).
    - **Algoritmia de IA** — Detección de comunidades con Louvain, Girvan-Newman,
      Greedy Modularity e InfoMap.
    """)

    st.info(
        "**Fuente de datos:** [Paleobiology Database](https://paleobiodb.org/) — "
        "registros del Triásico con coordenadas paleotectónicas reconstruidas por el "
        "modelo GPlates."
    )


# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 · PIPELINE DE DATOS (ETL)
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("## Pipeline de Datos (ETL)")
st.markdown("""
El pipeline completo se implementa en el cuaderno `EDA_01.ipynb` y transforma el dataset
crudo de la PBDB (más de 70 variables por registro) en un grafo ponderado listo para análisis
topológico.
""")

st.markdown("""
<div class="pipeline-container">
    <div class="pipeline-step">
        <div class="pipeline-num">1</div>
        <div class="pipeline-title">Carga PBDB</div>
        <div class="pipeline-desc">Descarga de registros del Triásico con &gt;70 variables. Se omiten 14 filas de metadatos.</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-num">2</div>
        <div class="pipeline-title">Limpieza</div>
        <div class="pipeline-desc">Selección de 7 variables clave. Eliminación de nulos estructurales. Extracción del género.</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-num">3</div>
        <div class="pipeline-title">Filtrado Terrestre</div>
        <div class="pipeline-desc">9 categorías de ambiente continental: terrestre, fluvial, lacustre, aluvial, eólico, etc.</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-num">4</div>
        <div class="pipeline-title">Grafo Bipartito</div>
        <div class="pipeline-desc">B&nbsp;=&nbsp;(U,&nbsp;V,&nbsp;E). U&nbsp;=&nbsp;yacimientos, V&nbsp;=&nbsp;géneros. Arista si el género aparece en el yacimiento.</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-num">5</div>
        <div class="pipeline-title">Proyección Unipartita</div>
        <div class="pipeline-desc">Proyección ponderada sobre U. Peso = nº de géneros compartidos entre yacimientos.</div>
    </div>
    <div class="pipeline-arrow">→</div>
    <div class="pipeline-step">
        <div class="pipeline-num">6</div>
        <div class="pipeline-title">Poda (Pruning)</div>
        <div class="pipeline-desc">Eliminación de aristas con peso&nbsp;=&nbsp;1 (75% de conexiones, géneros cosmopolitas).</div>
    </div>
</div>
""", unsafe_allow_html=True)

with st.expander("Justificación de la poda (peso > 1)"):
    st.markdown("""
    La distribución de pesos muestra que el **75 % de las aristas tienen peso 1**
    (un único género compartido). Estas conexiones débiles reflejan mayoritariamente
    co-ocurrencias de géneros cosmopolitas que aportan más ruido que señal biogeográfica.

    El umbral de poda elimina todas las aristas con *w* ≤ 1. Esta decisión se valida
    posteriormente mediante un **análisis de sensibilidad** que demuestra
    que las comunidades principales se mantienen estables con umbrales entre 2 y 4.
    """)


# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 · ANÁLISIS TOPOLÓGICO Y COMUNIDADES
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("## Análisis Topológico y Comunidades")

tab_metricas, tab_modelos, tab_comunidades, tab_sensibilidad = st.tabs([
    "Métricas de la Red",
    "Modelos Nulos",
    "Detección de Comunidades",
    "Análisis de Sensibilidad",
])

with tab_metricas:
    st.markdown("### Métricas Topológicas Principales")
    st.markdown("""
    La siguiente tabla resume las propiedades estructurales de la red biogeográfica
    resultante tras la poda. Todas las métricas posicionales se calculan sobre la
    componente gigante.
    """)

    df_metricas = pd.DataFrame({
        "Métrica": [
            "Nodos (yacimientos)", "Aristas (conexiones)",
            "Componentes conexas", "Componente gigante",
            "Grado medio ⟨k⟩", "Grado máximo",
            "Clustering global (transitividad)",
            "Distancia geodésica media", "Diámetro",
            "Asortatividad por grado", "Clique máximo",
        ],
        "Valor": [
            "943", "9.210",
            "23", "883 nodos (93,6 %)",
            "19,53", "188",
            "0,5277",
            "4,09", "12",
            "0,0646 (neutra)", "36 nodos",
        ],
        "Interpretación": [
            "Yacimientos terrestres del Triásico tras filtrado y poda.",
            "Pares de yacimientos que comparten ≥ 2 géneros fósiles.",
            "La red no es totalmente conexa; existen clusters aislados.",
            "El 93,6 % de los yacimientos forman una única componente.",
            "Cada yacimiento comparte géneros con ~20 otros en promedio.",
            "El hub más conectado comparte fauna con 188 yacimientos.",
            "Alta cohesión local: vecindarios biogeográficos densos.",
            "Cualquier par de yacimientos separado por ~4 saltos.",
            "Camino más largo posible en la componente gigante.",
            "No hay preferencia de conexión por grado similar.",
            "36 yacimientos forman un subgrafo completo.",
        ],
    })

    st.dataframe(
        df_metricas,
        use_container_width=True,
        hide_index=True,
        column_config={
            "Métrica": st.column_config.TextColumn(width="medium"),
            "Valor": st.column_config.TextColumn(width="small"),
            "Interpretación": st.column_config.TextColumn(width="large"),
        },
    )

    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown("""
        <div style="background:rgba(214,40,40,0.08); border:1px solid rgba(214,40,40,0.25);
        border-radius:10px; padding:16px; text-align:center;">
            <div style="font-size:2.2rem; font-weight:900; color:#d62828;
            font-family:'Playfair Display',serif;">22×</div>
            <div style="color:#94a3b8; font-size:0.85rem;">Clustering superior al azar<br>
            (0,528 vs. 0,023 en Erdős-Rényi)</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div style="background:rgba(247,127,0,0.08); border:1px solid rgba(247,127,0,0.25);
        border-radius:10px; padding:16px; text-align:center;">
            <div style="font-size:2.2rem; font-weight:900; color:#f77f00;
            font-family:'Playfair Display',serif;">4,09</div>
            <div style="color:#94a3b8; font-size:0.85rem;">Distancia geodésica media<br>
            (propiedad <em>small-world</em>)</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div style="background:rgba(42,157,143,0.08); border:1px solid rgba(42,157,143,0.25);
        border-radius:10px; padding:16px; text-align:center;">
            <div style="font-size:2.2rem; font-weight:900; color:#2a9d8f;
            font-family:'Playfair Display',serif;">lognormal</div>
            <div style="color:#94a3b8; font-size:0.85rem;">Mejor ajuste de la distribución<br>
            de grados (α = 2,67)</div>
        </div>
        """, unsafe_allow_html=True)

with tab_modelos:
    st.markdown("### Comparación con Modelos Nulos")
    st.markdown("""
    Para determinar si las propiedades topológicas son estadísticamente inusuales,
    se generaron **30 redes sintéticas** por cada modelo con los mismos parámetros.
    """)

    df_modelos_data = pd.DataFrame({
        "Modelo": ["Pangea (real)", "Erdős-Rényi", "Barabási-Albert", "Watts-Strogatz"],
        "Clustering (C)": [0.5277, 0.023, 0.058, 0.512],
        "Dist. media (L)": [4.09, 2.57, 2.53, 3.14],
    })

    col_tabla, col_chart = st.columns([2, 3])

    with col_tabla:
        st.markdown("#### Tabla Comparativa (*N* = 30 redes por modelo)")
        st.dataframe(df_modelos_data, hide_index=True, use_container_width=True)
        st.markdown("""
        **Conclusión:** El clustering real (0,53) es **22 veces superior** al de
        Erdős-Rényi, mientras que la distancia media (4,09) se mantiene corta.
        Firma inequívoca de una **red *small-world***.
        """)

    with col_chart:
        modelos_chart = ["Pangea", "Erdős-Rényi", "Barabási-Albert", "Watts-Strogatz"]
        clustering_vals = [0.5277, 0.023, 0.058, 0.512]
        colores = ["#2a9d8f", "#d62828", "#f77f00", "#003049"]

        fig_modelos = go.Figure()
        fig_modelos.add_trace(go.Bar(
            x=modelos_chart, y=clustering_vals,
            marker_color=colores, opacity=0.85,
            text=[f"{v:.3f}" for v in clustering_vals],
            textposition="outside",
            textfont=dict(color="#c8d6e5", size=12),
        ))
        fig_modelos.update_layout(
            title=dict(text="Coeficiente de Clustering por Modelo",
                       font=dict(color="#5eead4", size=15, family="Source Sans 3")),
            yaxis=dict(title="C", gridcolor="rgba(255,255,255,0.05)",
                       color="#94a3b8", range=[0, 0.65]),
            xaxis=dict(color="#94a3b8"),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Source Sans 3", color="#c8d6e5"),
            height=380, margin=dict(t=50, b=30),
            showlegend=False,
        )
        st.plotly_chart(fig_modelos, use_container_width=True)

with tab_comunidades:
    st.markdown("### Comparación de Algoritmos de Detección de Comunidades")
    st.markdown("""
    Se aplican tres algoritmos vistos en la asignatura, más InfoMap como referencia
    adicional basada en flujo de información.
    """)

    df_algos = pd.DataFrame({
        "Algoritmo": [
            "Louvain (comp. gigante)", "Greedy Modularity",
            "Girvan-Newman (subgrafo 150)", "InfoMap",
        ],
        "Comunidades": [14, 11, "variable", "~20"],
        "Modularidad (Q)": ["0,7186", "0,6964", "> 0,3", "0,66 (aprox.)"],
        "Tipo": ["Bottom-up heurístico", "Aglomerativo (Newman 2004)",
                 "Divisivo (edge betweenness)", "Flujo de información"],
    })
    st.dataframe(df_algos, hide_index=True, use_container_width=True)

    st.markdown("""
    **Louvain** obtiene la mayor modularidad (*Q* = 0,72), seguido de Greedy Modularity
    (*Q* = 0,70). Se detectan **5 macro-biomas principales** que agrupan el 76 % de
    los yacimientos.
    """)

    fig_q = go.Figure()
    nombres_algo = ["Louvain", "Greedy Mod.", "Girvan-Newman\n(sub.150)", "InfoMap"]
    valores_q = [0.7186, 0.6964, 0.45, 0.66]

    fig_q.add_trace(go.Bar(
        x=nombres_algo, y=valores_q,
        marker=dict(
            color=["#2a9d8f", "#003049", "#f77f00", "#d62828"],
            line=dict(color="rgba(255,255,255,0.15)", width=1),
        ),
        text=[f"Q = {v:.2f}" for v in valores_q],
        textposition="outside",
        textfont=dict(size=13, color="#c8d6e5"),
    ))
    fig_q.add_hline(y=0.3, line_dash="dash", line_color="#d62828",
                    annotation_text="Umbral de Newman (Q = 0.3)",
                    annotation_font=dict(color="#d62828", size=11))
    fig_q.update_layout(
        yaxis=dict(title="Modularidad (Q)", range=[0, 0.85],
                   gridcolor="rgba(255,255,255,0.05)", color="#94a3b8"),
        xaxis=dict(color="#94a3b8"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Source Sans 3", color="#c8d6e5"),
        height=380, margin=dict(t=20, b=30),
        showlegend=False,
    )
    st.plotly_chart(fig_q, use_container_width=True)

    st.markdown("### Nodos Clave de la Red")
    n_col1, n_col2 = st.columns(2)
    with n_col1:
        st.markdown("""
        **Hubs Biogeográficos** — Yacimientos con grado superior a 100 que actúan como
        centros de diversidad fósil. Se concentran en las placas tectónicas 101
        (Laurentia/Norteamérica) y 701 (China).
        """)
    with n_col2:
        st.markdown("""
        **Puentes entre Biomas** — Yacimientos con alta *betweenness centrality* pero
        grado moderado. Conectan comunidades distintas y podrían representar **ecotonos**.
        """)

with tab_sensibilidad:
    st.markdown("### Sensibilidad al Parámetro de Resolución (γ)")
    st.markdown("""
    El parámetro de resolución *γ* de Louvain controla la granularidad. Un barrido
    de *γ* entre 0,5 y 3,0 muestra estabilidad en el rango 0,75–1,5.
    """)

    df_res = pd.DataFrame({
        "γ": [0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5, 3.0],
        "Comunidades": [8, 10, 14, 16, 19, 25, 30, 38],
        "Q": [0.64, 0.68, 0.72, 0.70, 0.67, 0.61, 0.55, 0.48],
    })

    fig_sens = go.Figure()
    fig_sens.add_trace(go.Scatter(
        x=df_res["γ"], y=df_res["Q"],
        mode="lines+markers", name="Modularidad (Q)",
        line=dict(color="#2a9d8f", width=3),
        marker=dict(size=10, color="#2a9d8f", line=dict(color="#f0f9ff", width=2)),
        yaxis="y1",
    ))
    fig_sens.add_trace(go.Bar(
        x=df_res["γ"], y=df_res["Comunidades"],
        name="Nº Comunidades", opacity=0.3,
        marker_color="#7dd3fc",
        yaxis="y2",
    ))
    fig_sens.update_layout(
        yaxis=dict(title="Modularidad (Q)", color="#2a9d8f",
                   gridcolor="rgba(255,255,255,0.05)", range=[0.3, 0.8]),
        yaxis2=dict(title="Nº Comunidades", color="#7dd3fc",
                    overlaying="y", side="right", range=[0, 50]),
        xaxis=dict(title="Resolución (γ)", color="#94a3b8"),
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Source Sans 3", color="#c8d6e5"),
        legend=dict(x=0.7, y=1.1, orientation="h", font=dict(color="#c8d6e5")),
        height=380, margin=dict(t=30, b=40),
    )
    st.plotly_chart(fig_sens, use_container_width=True)

    st.markdown("""
    **Sensibilidad al umbral de poda:** las comunidades principales se mantienen
    estables con umbrales de peso mínimo entre 2 y 4. La convergencia de tres
    algoritmos independientes sobre *Q* > 0,3 refuerza que la estructura es genuina.
    """)


# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 5 · VISUALIZACIÓN INTERACTIVA DE LA RED
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("## Visualización Interactiva de la Red")

# ┌────────────────────────────────────────────────────────────────────┐
# │ Coloca 'red_pangea_interactiva.html' junto a app.py              │
# │ Generado con pyvis en tus notebooks.                              │
# │ Se ofrece como descarga para evitar congelar Streamlit.          │
# └────────────────────────────────────────────────────────────────────┘

RUTA_RED_HTML = "extras/mapa_pangea_interactivo.html"

if os.path.exists(RUTA_RED_HTML):
    st.markdown("""
    Mapa interactivo con las comunidades de Louvain proyectadas sobre las
    paleo-coordenadas de Pangea (izquierda) y las coordenadas modernas
    post-deriva continental (derecha).
    """)

    with open(RUTA_RED_HTML, "r", encoding="utf-8") as f:
        html_content = f.read()

    st.download_button(
        label="Descargar Red Interactiva (HTML)",
        data=html_content,
        file_name="red_pangea_interactiva.html",
        mime="text/html",
    )
    st.caption("Descarga el archivo y ábrelo en tu navegador para explorarlo sin limitaciones de rendimiento.")

else:
    st.warning(
        "**Archivo de red no encontrado.** Coloca `red_pangea_interactiva.html` "
        "en la misma carpeta que `app.py` para habilitar la descarga."
    )

    st.markdown("""
    <div style="background:rgba(0,48,73,0.15); border:2px dashed rgba(42,157,143,0.3);
    border-radius:16px; padding:60px 40px; text-align:center; margin:20px 0;">
        <div style="font-size:3rem;">🕸️</div>
        <div style="color:#5eead4; font-size:1.1rem; font-weight:600; margin:8px 0;">
            Red Interactiva de Pangea
        </div>
        <div style="color:#64748b; font-size:0.85rem;">
            943 nodos · 9.210 aristas · Comunidades de Louvain<br>
            <code>red_pangea_interactiva.html</code>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 6 · CONCLUSIONES Y SESGO
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("## Conclusiones y Sesgo de Muestreo")

conc_col1, conc_col2 = st.columns([3, 2])

with conc_col1:
    st.markdown("### Conclusiones Principales")
    st.markdown("""
    1. **Biomas diferenciados en Pangea.** A pesar de la continuidad continental, la red
       presenta una modularidad *Q* = 0,72 que indica una partición marcada de la fauna
       en macro-biomas terrestres.

    2. **Propiedades de mundo pequeño (*small-world*).** El clustering es 22× superior
       al azar, combinado con distancias geodésicas cortas (media 4,09). Refleja
       vecindades biogeográficas cohesivas conectadas por corredores faunísticos.

    3. **Distribución de cola pesada.** El mejor ajuste de la distribución de grados es
       lognormal (α = 2,67), indicando la existencia de *hubs* paleontológicos.

    4. **Fragmentación por deriva continental.** La proyección sobre coordenadas modernas
       muestra la dispersión de los biomas originales por múltiples continentes actuales.

    5. **Convergencia algorítmica.** Tres algoritmos independientes (Louvain, Greedy,
       Girvan-Newman) convergen sobre *Q* > 0,3, reforzando que la estructura es genuina.
    """)

with conc_col2:
    st.markdown("### Sesgo de Muestreo Paleontológico")

    st.markdown("""
    <div style="background:rgba(214,40,40,0.06); border:1px solid rgba(214,40,40,0.2);
    border-radius:10px; padding:16px; margin-bottom:16px;">
        <div style="color:#f77f00; font-weight:700; margin:0 0 6px 0;">
            Sesgo Identificado
        </div>
        <div style="font-size:0.92rem;">
            Las tres placas más excavadas (101-Norteamérica, 701-China, 305-Europa)
            concentran el <strong>60 %</strong> de los yacimientos.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    Un **test de Chi-cuadrado** de independencia entre comunidades y placas tectónicas
    arroja un resultado altamente significativo (*p* < 0,001), pero el **coeficiente
    de Cramér *V*** = 0,43 indica una asociación moderada, no total.

    Esto sugiere que las comunidades reflejan una **combinación de señal biológica
    y artefacto geográfico**.
    """)

    st.markdown("""
    <div style="margin-top:12px;">
        <div style="color:#94a3b8; font-size:0.8rem;">Cramér V (asociación comunidad–placa)</div>
        <div style="background:rgba(255,255,255,0.06); border-radius:20px; height:20px;
        margin-top:4px; overflow:hidden; position:relative;">
            <div style="background: linear-gradient(90deg, #2a9d8f, #f77f00);
            width:43%; height:100%; border-radius:20px;"></div>
            <div style="position:absolute; right:8px; top:1px; color:#c8d6e5;
            font-size:0.75rem; font-weight:600;">V = 0,43</div>
        </div>
        <div style="display:flex; justify-content:space-between; margin-top:2px;">
            <div style="color:#64748b; font-size:0.7rem;">0 (independencia)</div>
            <div style="color:#64748b; font-size:0.7rem;">1 (asociación total)</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with st.expander("Limitaciones del Estudio"):
    st.markdown("""
    - La poda de aristas con peso 1 no se valida contra un *Configuration Model*.
    - Las paleo-coordenadas tienen incertidumbre inherente al modelo GPlates.
    - La resolución taxonómica a nivel de género puede enmascarar diferencias a nivel de especie.
    - Girvan-Newman se ejecutó sobre un subgrafo de 150 nodos por complejidad *O*(*m*²·*n*).
    """)


# ═════════════════════════════════════════════════════════════════════════════
# SECCIÓN 7 · HERRAMIENTAS Y CÓDIGO
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("## Herramientas y Código Fuente")

h_col1, h_col2, h_col3 = st.columns(3)

with h_col1:
    st.markdown("""
    ### Stack Técnico
    - **Python 3.11**
    - pandas · numpy
    - NetworkX
    - GeoPandas · Cartopy
    - matplotlib · Plotly
    - pyvis · Gephi 0.10
    - powerlaw · scipy
    - InfoMap
    """)

with h_col2:
    st.markdown("""
    ### Cuadernos Jupyter
    - `EDA_01.ipynb` — Pipeline ETL, construcción de la red, Louvain y
      visualización geográfica.
    - `Analisis_Topologico_Pangea.ipynb` — Métricas topológicas, modelos
      nulos, comparación de algoritmos, sensibilidad y sesgo.
    """)

with h_col3:
    st.markdown("""
    ### Referencias Clave
    - Blondel et al. (2008) — Louvain
    - Clauset et al. (2009) — Power-law
    - Girvan & Newman (2002)
    - Watts & Strogatz (1998) — Small-world
    - [Paleobiology Database](https://paleobiodb.org/)
    """)


# ═════════════════════════════════════════════════════════════════════════════
# FOOTER
# ═════════════════════════════════════════════════════════════════════════════

st.markdown("---")
st.markdown("""
<div style="text-align:center; padding:20px 0 30px 0;">
    <div style="color:#2a9d8f; font-family:'Playfair Display',serif;
    font-size:1.15rem; font-weight:700; margin-bottom:4px;">
        Análisis Topológico de Pangea
    </div>
    <div style="color:#475569; font-size:0.8rem;">
        Computación Social y Personalización · Grado en CDIA ·
        Universidad Politécnica de Madrid · 2025-2026
    </div>
</div>
""", unsafe_allow_html=True)
