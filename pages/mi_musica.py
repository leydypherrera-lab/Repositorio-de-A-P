import streamlit as st
from utils import cargar_datos, inicializar_estado, FEATURES

st.set_page_config(page_title="Mi Música", page_icon="🎧", layout="wide")
inicializar_estado()
df = cargar_datos()

st.title("🎧 Mi Música")

favoritos = st.session_state["favoritos"]
if not favoritos:
    st.info("Aún no has guardado canciones. Ve a Explorar o Jugar para añadir algunas.")
    st.stop()

mis = df.loc[favoritos]
st.write(f"Tienes **{len(mis)}** canciones guardadas.")

col1, col2 = st.columns([3, 2])
with col1:
    st.dataframe(
        mis[["song_name", "artist_name", "language", "genres_txt"]]
        .rename(columns={"song_name": "Canción", "artist_name": "Artista",
                         "language": "Idioma", "genres_txt": "Géneros"}),
        use_container_width=True, hide_index=True,
    )
with col2:
    st.subheader("Tu perfil sonoro")
    st.bar_chart(mis[FEATURES].mean())

st.subheader("Géneros que más guardas")
conteo = mis["genres_list"].explode().value_counts().head(8)
if not conteo.empty:
    st.bar_chart(conteo)

st.divider()
quitar = st.selectbox("Quitar una canción", [""] + [f"{r.song_name} — {r.artist_name}" for r in mis.itertuples()])
if quitar and st.button("Quitar"):
    idx = [i for i, r in mis.iterrows() if f"{r.song_name} — {r.artist_name}" == quitar][0]
    st.session_state["favoritos"].remove(idx)
    st.rerun()

st.download_button("Descargar mi lista (CSV)",
                   mis.drop(columns=["genres_list"]).to_csv(index=False).encode("utf-8"),
                   file_name="mi_musica.csv", mime="text/csv")