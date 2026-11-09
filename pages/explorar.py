import streamlit as st
from utils import cargar_datos, inicializar_estado, FEATURES

st.set_page_config(page_title="Explorar", page_icon="🔍", layout="wide")
inicializar_estado()
df = cargar_datos()

st.title("🔍 Explorar canciones")

# ---------- Filtros ----------
f1, f2, f3 = st.columns(3)
busqueda = f1.text_input("Buscar por canción o artista")
idiomas = f2.multiselect("Idioma", sorted(df["language"].unique()))
todos_generos = sorted({g for lista in df["genres_list"] for g in lista})
generos = f3.multiselect("Género", todos_generos)

pop_min, pop_max = st.slider("Popularidad del artista", 0, 100, (0, 100))

filtrado = df[df["new_artist_popularity"].between(pop_min, pop_max)]
if busqueda:
    mask = filtrado["song_name"].str.contains(busqueda, case=False, na=False) | \
           filtrado["artist_name"].str.contains(busqueda, case=False, na=False)
    filtrado = filtrado[mask]
if idiomas:
    filtrado = filtrado[filtrado["language"].isin(idiomas)]
if generos:
    filtrado = filtrado[filtrado["genres_list"].apply(lambda l: any(g in l for g in generos))]

st.write(f"**{len(filtrado)}** canciones encontradas")
st.dataframe(
    filtrado[["song_name", "artist_name", "language", "genres_txt", "new_artist_popularity"]]
    .rename(columns={
        "song_name": "Canción", "artist_name": "Artista", "language": "Idioma",
        "genres_txt": "Géneros", "new_artist_popularity": "Popularidad",
    }),
    use_container_width=True, hide_index=True,
)

# ---------- Detalle de una canción ----------
st.divider()
if not filtrado.empty:
    opciones = {f"{r.song_name} — {r.artist_name}": i for i, r in filtrado.iterrows()}
    elegida = st.selectbox("Ver detalle de una canción", list(opciones))
    cancion = df.loc[opciones[elegida]]

    st.subheader(f"{cancion.song_name}")
    st.caption(f"{cancion.artist_name} · {cancion.language} · {cancion.genres_txt}")

    cols = st.columns(len(FEATURES))
    for c, f in zip(cols, FEATURES):
        c.metric(f.capitalize(), f"{cancion[f]:.2f}")

    with st.expander("Ver letra"):
        st.text(cancion.lyrics)

    if opciones[elegida] in st.session_state["favoritos"]:
        st.success("Ya está en Mi Música ✅")
    elif st.button("❤️ Guardar en Mi Música"):
        st.session_state["favoritos"].append(opciones[elegida])
        st.rerun()



