import random
import streamlit as st
from utils import cargar_datos, inicializar_estado, FEATURES

st.set_page_config(page_title="Jugar", page_icon="🎲", layout="wide")
inicializar_estado()
df = cargar_datos()

RONDAS = 5
st.title("🎲 Esto o aquello")
st.write(f"Elige entre dos canciones en {RONDAS} rondas y te recomendaremos música parecida.")


def nueva_pareja():
    st.session_state["pareja"] = random.sample(range(len(df)), 2)


if "elegidas" not in st.session_state:
    st.session_state["elegidas"] = []
if "pareja" not in st.session_state:
    nueva_pareja()


def elegir(idx):
    st.session_state["elegidas"].append(idx)
    nueva_pareja()


ronda = len(st.session_state["elegidas"])

if ronda < RONDAS:
    st.progress(ronda / RONDAS, text=f"Ronda {ronda + 1} de {RONDAS}")
    cols = st.columns(2)
    for col, idx in zip(cols, st.session_state["pareja"]):
        c = df.loc[idx]
        with col:
            st.subheader(c.song_name)
            st.caption(f"{c.artist_name} · {c.genres_txt}")
            for f in FEATURES:
                st.write(f"{f.capitalize()}: {c[f]:.2f}")
                st.progress(float(c[f]))
            st.button("Elegir esta", key=f"btn_{idx}", on_click=elegir,
                      args=(idx,), use_container_width=True)
else:
    elegidas = df.loc[st.session_state["elegidas"]]
    perfil = elegidas[FEATURES].mean()

    st.success("¡Listo! Este es tu perfil musical:")
    st.bar_chart(perfil)

    # Recomendación: canciones más cercanas al perfil promedio
    candidatas = df.drop(index=st.session_state["elegidas"]).copy()
    candidatas["distancia"] = ((candidatas[FEATURES] - perfil) ** 2).sum(axis=1) ** 0.5
    recomendadas = candidatas.nsmallest(5, "distancia")

    st.subheader("Te recomendamos")
    for i, r in recomendadas.iterrows():
        a, b = st.columns([4, 1])
        a.write(f"**{r.song_name}** — {r.artist_name} ({r.genres_txt})")
        if i not in st.session_state["favoritos"]:
            if b.button("❤️ Guardar", key=f"rec_{i}"):
                st.session_state["favoritos"].append(i)
                st.rerun()
        else:
            b.write("✅ Guardada")

    if st.button("Jugar de nuevo"):
        st.session_state["elegidas"] = []
        nueva_pareja()
        st.rerun()