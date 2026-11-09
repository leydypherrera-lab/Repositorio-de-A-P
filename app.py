import streamlit as st
from utils import ASSETS, mostrar_imagen, inicializar_estado

st.set_page_config(page_title="Vibra Musical", page_icon="🎵", layout="wide")
inicializar_estado()

# Logo en la barra lateral (arriba del menú)
if (ASSETS / "logo.png").exists():
    st.logo(str(ASSETS / "logo.png"))

# ---------- Encabezado con logo ----------
col_logo, col_texto = st.columns([1, 4], vertical_alignment="center")
with col_logo:
    mostrar_imagen(ASSETS / "logo.png", width=160)
with col_texto:
    st.title("Vibra Musical")
    st.write(
        "Vibra Musical es un espacio para explorar canciones y descubrir "
        "nueva música a través de sus características y géneros."
    )

st.divider()

# ---------- Tres secciones ----------
c1, c2, c3 = st.columns(3)
with c1:
    st.subheader("🔍 Explora canciones")
    st.write("Descubre nuestro catálogo y encuentra algo que quieras escuchar.")
    if st.button("Explorar canciones", use_container_width=True):
        st.switch_page("pages/1_Explorar.py")
with c2:
    st.subheader("🎲 Esto o aquello")
    st.write("¿No sabes qué escuchar? ¡Descubre tu próxima canción jugando!")
    if st.button("Jugar", use_container_width=True):
        st.switch_page("pages/2_Jugar.py")
with c3:
    st.subheader("🎧 Mi Música")
    st.write("Guarda canciones y descubre tus preferencias musicales.")
    if st.button("Ver mi música", use_container_width=True):
        st.switch_page("pages/3_Mi_Musica.py")

st.divider()

# ---------- 3 biografías con fotos ----------
st.header("Nuestro equipo")

integrantes = [
    {
        "nombre": "Nombre Integrante 1",
        "foto": "integrante1.jpg",
        "rol": "Estudiante de Ingeniería Industrial",
        "bio": "Escribe aquí una biografía corta: de dónde eres, qué estudias, "
               "qué parte del proyecto desarrollaste y qué música te gusta.",
    },
    {
        "nombre": "Nombre Integrante 2",
        "foto": "integrante2.jpg",
        "rol": "Estudiante de Ingeniería Industrial",
        "bio": "Escribe aquí una biografía corta: de dónde eres, qué estudias, "
               "qué parte del proyecto desarrollaste y qué música te gusta.",
    },
    {
        "nombre": "Nombre Integrante 3",
        "foto": "integrante3.jpg",
        "rol": "Estudiante de Ingeniería Industrial",
        "bio": "Escribe aquí una biografía corta: de dónde eres, qué estudias, "
               "qué parte del proyecto desarrollaste y qué música te gusta.",
    },
]

for col, p in zip(st.columns(3), integrantes):
    with col:
        mostrar_imagen(ASSETS / p["foto"], use_container_width=True)
        st.subheader(p["nombre"])
        st.caption(p["rol"])
        st.write(p["bio"])