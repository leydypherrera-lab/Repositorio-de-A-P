import pandas as pd
import streamlit as st

from src.data import cargar_datos

st.title("❤️ Mi Música")
df = cargar_datos()

# Lista de favoritas guardada en la sesión
if "favoritas" not in st.session_state:
    st.session_state.favoritas = []

tab1, tab2, tab3 = st.tabs(["⭐ Mis favoritas", "➕ Agregar canción propia", "📁 Sobre los datos"])

with tab1:
    opciones = (df["titulo"] + " — " + df["artista"]).tolist()
    elegidas = st.multiselect("Elige tus canciones favoritas del catálogo", opciones)
    if elegidas:
        favs = df[(df["titulo"] + " — " + df["artista"]).isin(elegidas)]
    else:
        favs = df.iloc[0:0]
    propias = pd.DataFrame(st.session_state.favoritas)
    todas = pd.concat([favs[["titulo", "artista", "genero", "anio"]], propias], ignore_index=True)

    if todas.empty:
        st.info("Aún no tienes favoritas. ¡Elige algunas arriba!")
    else:
        st.dataframe(todas, use_container_width=True, hide_index=True)
        st.subheader("Tus géneros favoritos")
        st.bar_chart(todas["genero"].value_counts())
        st.download_button(
            "⬇️ Descargar mis favoritas (CSV)",
            todas.to_csv(index=False).encode("utf-8"),
            file_name="mis_favoritas.csv",
            mime="text/csv",
        )

with tab2:
    with st.form("nueva_cancion", clear_on_submit=True):
        titulo = st.text_input("Título")
        artista = st.text_input("Artista")
        genero = st.selectbox("Género", sorted(df["genero"].unique()))
        anio = st.number_input("Año", min_value=1900, max_value=2030, value=2020, step=1)
        enviado = st.form_submit_button("Agregar")
    if enviado:
        if titulo.strip() and artista.strip():
            st.session_state.favoritas.append(
                {"titulo": titulo.strip(), "artista": artista.strip(),
                 "genero": genero, "anio": int(anio)}
            )
            st.success("Canción agregada. Mira la pestaña “Mis favoritas”.")
        else:
            st.error("Escribe el título y el artista.")

with tab3:
    st.write(f"El catálogo tiene **{df.shape[0]} filas** y **{df.shape[1]} columnas**.")
    st.write("Valores nulos por columna:")
    st.dataframe(df.isna().sum().rename("nulos"))
    st.write("Vista previa:")
    st.dataframe(df.head(10), hide_index=True)
