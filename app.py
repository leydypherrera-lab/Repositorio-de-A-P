"""Vibra Musical - punto de entrada.
Ejecutar con:  streamlit run app.py
"""
from pathlib import Path

import streamlit as st

RAIZ = Path(__file__).resolve().parent

# set_page_config se llama UNA sola vez, aquí (no en las páginas)
st.set_page_config(
    page_title="Vibra Musical",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Estilos propios
css = RAIZ / "assets" / "estilos.css"
if css.exists():
    st.markdown(f"<style>{css.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)

# Logo en la barra lateral
logo = RAIZ / "assets" / "logo.png"
if logo.exists():
    st.logo(str(logo))

# Navegación entre páginas (carpeta pages/)
paginas = [
    st.Page("pages/inicio.py", title="Inicio", icon="🏠", default=True),
    st.Page("pages/explorar.py", title="Explorar", icon="🔎"),
    st.Page("pages/jugar.py", title="Jugar", icon="🎮"),
    st.Page("pages/mi_musica.py", title="Mi música", icon="❤️"),
]
st.navigation(paginas).run()
