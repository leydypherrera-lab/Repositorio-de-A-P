import streamlit as st

from src.data import cargar_datos, filtrar

st.title("🔎 Explorar canciones")
df = cargar_datos()

# --- Filtros en la barra lateral ---
st.sidebar.header("Filtros")
generos = st.sidebar.multiselect("Género", sorted(df["genero"].unique()))
anio_min, anio_max = int(df["anio"].min()), int(df["anio"].max())
rango = st.sidebar.slider("Años", anio_min, anio_max, (anio_min, anio_max))
texto = st.sidebar.text_input("Buscar título o artista")

res = filtrar(df, generos, rango, texto)
st.write(f"**{len(res)}** canciones encontradas")

tab1, tab2 = st.tabs(["📋 Tabla", "📊 Gráficos"])

with tab1:
    st.dataframe(
        res[["titulo", "artista", "genero", "anio"]].rename(
            columns={"titulo": "Título", "artista": "Artista", "genero": "Género", "anio": "Año"}
        ),
        use_container_width=True,
        hide_index=True,
    )

with tab2:
    if res.empty:
        st.warning("No hay datos con esos filtros.")
    else:
        izq, der = st.columns(2)
        with izq:
            st.subheader("Canciones por género")
            st.bar_chart(res["genero"].value_counts())
        with der:
            st.subheader("Canciones por década")
            st.bar_chart(res["decada"].value_counts().sort_index())
        st.subheader("Artistas con más canciones")
        st.bar_chart(res["artista"].value_counts().head(10))
