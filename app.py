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

st.markdown(
    """
    <div style="text-align: center; color: #9a8fb8; font-size: 0.85rem; margin-top: 3rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1);">
        © 2026 Leydy y Katherine · Vibra Musical · 
        <a href="https://creativecommons.org/licenses/by-sa/4.0/" target="_blank" style="color: #8ab4f8; text-decoration: underline;">
            Creative Commons BY-SA 4.0
        </a>
    </div>
    """,
    unsafe_allow_html=True,
)