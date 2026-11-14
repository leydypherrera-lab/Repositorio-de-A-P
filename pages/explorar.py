### PREPARACIÓN DEL ENTORNO
import os
import urllib.parse
import streamlit as st
import plotly.express as px
import pandas as pd

# Cargar estilos personalizados del proyecto si existen
if os.path.exists("assets/estilos.css"):
    with open("assets/estilos.css", encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


### CARGA DE DATOS
@st.cache_data
def cargar_canciones():
    df = pd.read_csv("data/datos.csv")

    # Normalizar nombres de columnas (por si tienen tildes, mayúsculas o están en inglés)
    mapa_columnas = {}
    for col in df.columns:
        c = col.strip().lower()
        if c in ["titulo", "título", "title", "cancion", "canción"]:
            mapa_columnas[col] = "titulo"
        elif c in ["artista", "artist", "cantante"]:
            mapa_columnas[col] = "artista"
        elif c in ["genero", "género", "genre"]:
            mapa_columnas[col] = "genero"
        elif c in ["anio", "año", "year", "fecha"]:
            mapa_columnas[col] = "anio"

    df = df.rename(columns=mapa_columnas)
    df["anio"] = pd.to_numeric(df["anio"], errors="coerce")
    df = df.dropna(subset=["anio"]).copy()
    df["anio"] = df["anio"].astype(int)
    df["decada"] = (df["anio"] // 10) * 10
    df = df.reset_index(drop=True)
    df["id"] = df.index
    return df


def filtrar_canciones(df, titulo="", genero="Todos", artista="", rango_anios=None):
    resultado = df.copy()

    if titulo.strip():
        resultado = resultado[
            resultado["titulo"].str.contains(titulo.strip(), case=False, na=False)
        ]

    if genero != "Todos":
        resultado = resultado[resultado["genero"] == genero]

    if artista.strip():
        resultado = resultado[
            resultado["artista"].str.contains(artista.strip(), case=False, na=False)
        ]

    if rango_anios is not None:
        resultado = resultado[
            (resultado["anio"] >= rango_anios[0])
            & (resultado["anio"] <= rango_anios[1])
        ]

    return resultado.reset_index(drop=True)


canciones = cargar_canciones()  # Cargar las canciones desde el archivo CSV


### INICIALIZACIÓN DE VARIABLES DE SESIÓN
if "canciones_favoritas" not in st.session_state:
    st.session_state["canciones_favoritas"] = []

if "canciones_escuchadas" not in st.session_state:
    st.session_state["canciones_escuchadas"] = []


### ESTRUCTURA VISUAL DE LA PÁGINA
st.title("🔍 Explorar")


## FILTROS DE BÚSQUEDA
# ------------------------------------------------------------------------------
titulo_buscar = st.text_input(
    "Buscar por título:", placeholder="Escribe el título de la canción..."
)

col1, col2, col3 = st.columns(3)
with col1:
    lista_generos = ["Todos"] + sorted(canciones["genero"].dropna().unique().tolist())
    search_genre = st.selectbox(
        "🎭 Género",
        options=lista_generos,
        index=0,
    )

with col2:
    search_artist = st.text_input(
        "🎤 Artista",
        placeholder="Ej. Queen, Michael Jackson",
    )

with col3:
    anio_min = int(canciones["anio"].min())
    anio_max = int(canciones["anio"].max())
    search_years = st.slider(
        "📅 Rango de años",
        min_value=anio_min,
        max_value=anio_max,
        value=(anio_min, anio_max),
    )

canciones_filtradas = filtrar_canciones(
    canciones,
    titulo=titulo_buscar,
    genero=search_genre,
    artista=search_artist,
    rango_anios=search_years,
)


# PRESENTACIÓN DE RESULTADOS EN TABLA FILTRADA
# ------------------------------------------------------------------------------
st.divider()
st.subheader(f"{len(canciones_filtradas):,} canciones encontradas")

if canciones_filtradas.empty:
    st.warning("No se encontraron canciones con los filtros seleccionados. Intenta ampliar tu búsqueda.")
    st.stop()

opciones = {  # opciones de cantidad de resultados a mostrar
    "10 canciones": 10,
    "50 canciones": 50,
    "100 canciones": 100,
    "Todas las canciones": len(canciones_filtradas),
}

seleccion = st.selectbox(
    "Mostrando las primeras...",
    options=list(opciones.keys()),
    help="Selecciona la cantidad de resultados a mostrar",
    index=1,
)

cant_canciones_mostrar = opciones[seleccion]
nombres_columnas = {
    "id": "id",
    "titulo": "🎵 Canción",
    "artista": "🎤 Artista",
    "genero": "🎭 Género",
    "anio": "📅 Año",
    "decada": "🕰️ Década",
}

tabla_mostrar = (
    canciones_filtradas[nombres_columnas.keys()]
    .head(cant_canciones_mostrar)
    .rename(columns=nombres_columnas)
)

eventos_tabla = st.dataframe(
    tabla_mostrar,
    width="stretch",
    hide_index=True,
    on_select="rerun",  # Controla qué sucede cuando el usuario selecciona una fila
    selection_mode="single-row",  # Para seleccionar una sola fila a la vez
    column_config={"id": None},  # Oculta la columna "id" de la tabla
)


## PRESENTACIÓN DE DETALLES DE LA CANCIÓN SELECCIONADA
# ------------------------------------------------------------------------------
if eventos_tabla.selection.rows:
    st.info("🎵 Ésta es la canción que escogiste:")

    cancion = canciones_filtradas.iloc[eventos_tabla.selection.rows[0]]
    total_artista = int((canciones["artista"] == cancion["artista"]).sum())
    total_genero = int((canciones["genero"] == cancion["genero"]).sum())
    antiguedad = 2026 - int(cancion["anio"])
    query_yt = urllib.parse.quote(f"{cancion['titulo']} {cancion['artista']}")
    url_youtube = f"https://www.youtube.com/results?search_query={query_yt}"

    col_izq, col_der = st.columns([1, 2])
    with col_izq:
        st.markdown(
            f"""
            <div style="
                background: linear-gradient(135deg, #4c1d95, #1e1b4b);
                border: 1px solid #8b5cf6;
                border-radius: 14px;
                padding: 24px 16px;
                text-align: center;
                color: white;
            ">
                <div style="font-size: 54px; margin-bottom: 8px;">💿</div>
                <div style="font-weight: 700; font-size: 16px;">{cancion['titulo']}</div>
                <div style="color: #c4b5fd; font-size: 14px; margin-top: 4px;">{cancion['artista']}</div>
                <div style="margin-top: 12px; font-size: 12px; background: rgba(139,92,246,0.25); padding: 4px 10px; border-radius: 999px; display: inline-block;">
                    {cancion['genero']} • {cancion['anio']}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.markdown(f"[▶️ Escuchar en YouTube]({url_youtube})")

    with col_der:
        st.subheader(cancion["titulo"])
        st.caption(f"Interpretada por {cancion['artista']} — Clásico de los años {cancion['decada']}s")

        artista_txt = f"🎤 Artista: {cancion['artista']}"
        genero_txt = f"🎭 Género: {cancion['genero']}"
        anio_txt = f"📅 Año: {cancion['anio']} ({antiguedad} años)"
        decada_txt = f"🕰️ Década: {cancion['decada']}s"
        cat_artista = f"💿 En catálogo (artista): {total_artista} canción(es)"
        cat_genero = f"🎶 En catálogo (género): {total_genero} canción(es)"

        st.markdown(
            f"""
            |||
            | :--- | :--- |
            | {artista_txt} | {genero_txt} |
            | {anio_txt} | {decada_txt} |
            | {cat_artista} | {cat_genero} |
            """
        )

        id_cancion = int(cancion["id"])

        boton_1, boton_2 = st.columns(2)
        with boton_1:
            if id_cancion in st.session_state["canciones_favoritas"]:
                st.success("❤️ Guardada en tus favoritas")
            elif st.button("❤️ Guardar en favoritas", width="stretch"):
                st.session_state["canciones_favoritas"].append(id_cancion)
                st.rerun()

        with boton_2:
            if id_cancion in st.session_state["canciones_escuchadas"]:
                st.success("✅ Marcada como escuchada")
            elif st.button("✅ Ya la escuché", width="stretch"):
                st.session_state["canciones_escuchadas"].append(id_cancion)
                st.rerun()
else:
    st.info("👆 Selecciona una canción en la tabla para ver más detalles.")


## ESTADÍSTICAS DESCRIPTIVAS Y VISUALIZACIÓN DE GRÁFICOS DEL DATAFRAME
# ------------------------------------------------------------------------------
if canciones_filtradas.shape[0] > 0:
    st.divider()
    st.subheader(f"Estadísticas de {canciones_filtradas.shape[0]:,} canciones")

    # -------- Resumen de los filtros aplicados --------
    filtros_activos = []

    if titulo_buscar.strip():
        filtros_activos.append(f"Título: {titulo_buscar.strip()}")

    if search_genre != "Todos":
        filtros_activos.append(f"Género: {search_genre}")

    if search_artist.strip():
        filtros_activos.append(f"Artista: {search_artist.strip()}")

    if search_years != (anio_min, anio_max):
        filtros_activos.append(f"Años: {search_years[0]}–{search_years[1]}")

    if filtros_activos:
        st.info("**Filtros |** " + " | ".join(filtros_activos))
    else:
        st.info("No hay filtros aplicados | Mostrando todas las canciones.")

    # -------- Indicadores descriptivos (4 métricas dinámicas) --------
    porcentaje_cat = (len(canciones_filtradas) / len(canciones)) * 100
    genero_top = canciones_filtradas["genero"].value_counts().idxmax()
    anio_promedio = int(round(canciones_filtradas["anio"].mean()))

    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total seleccionadas", f"{len(canciones_filtradas)}", f"{porcentaje_cat:.1f}% del catálogo")
    m2.metric("Artistas únicos", f"{canciones_filtradas['artista'].nunique()}")
    m3.metric("Géneros activos", f"{canciones_filtradas['genero'].nunique()}")
    m4.metric("Género predominante", genero_top, f"Año promedio: {anio_promedio}")

    # -------- Gráficos interactivos con Plotly --------
    top_artistas = (
        canciones_filtradas["artista"]
        .value_counts()
        .head(10)
        .reset_index()
    )
    top_artistas.columns = ["Artista", "Canciones"]
    fig_artistas = px.bar(
        top_artistas,
        x="Canciones",
        y="Artista",
        orientation="h",
        title="Top 10 artistas con más canciones en la selección",
        color="Canciones",
        color_continuous_scale="Purples",
    )
    fig_artistas.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
    st.plotly_chart(fig_artistas, width="stretch")

    col_g1, col_g2 = st.columns(2)

    with col_g1:
        por_genero = canciones_filtradas["genero"].value_counts().reset_index()
        por_genero.columns = ["Género", "Canciones"]
        fig_genero = px.bar(
            por_genero,
            x="Género",
            y="Canciones",
            title="Distribución de canciones por género",
            color_discrete_sequence=["#8B5CF6"],
        )
        st.plotly_chart(fig_genero, width="stretch")

    with col_g2:
        por_decada = (
            canciones_filtradas.groupby("decada")
            .size()
            .reset_index(name="Canciones")
        )
        por_decada["Década"] = por_decada["decada"].astype(str) + "s"
        fig_decada = px.bar(
            por_decada,
            x="Década",
            y="Canciones",
            title="Distribución de canciones por década",
            color_discrete_sequence=["#A855F7"],
        )
        st.plotly_chart(fig_decada, width="stretch")