
import streamlit as st
import base64
import mimetypes
import html

from src.data import buscar_imagen, cargar_datos, resumen

df = cargar_datos()
r = resumen(df)

#Diseño

st.markdown("""
<style>

/* Fondo general */
.stApp {
    background: linear-gradient(135deg, #0b0618, #160b30, #0b0618);
}

/* Ampliar el contenido */
.block-container {
    max-width: 1500px !important;
    padding-top: 2rem;
    padding-bottom: 3rem;
    padding-left: 3rem;
    padding-right: 3rem;
}

/* Titulo principal */
.vm-hero {
    background: linear-gradient(120deg, #281052, #551a91, #24104b);
    border: 1px solid #9747ff;
    border-radius: 22px;
    padding: 35px;
    margin-bottom: 25px;
    box-shadow: 0 0 25px rgba(153, 70, 255, 0.25);
}

.vm-hero h1 {
    font-size: 55px;
    font-weight: 850;
    color: white;
    margin: 0;
}

.vm-hero p {
    color: #e4d6ff;
    font-size: 19px;
    margin-top: 12px;
}

/* Logo */
.vm-logo {
    display: flex;
    align-items: center;
    gap: 18px;
}

.vm-logo svg {
    width: 85px;
    height: 85px;
    flex-shrink: 0;
}

.vm-logo span {
    background: linear-gradient(90deg, #ffffff, #e1a1ff, #a76aff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Estadisticas */
div[data-testid="stMetric"] {
    background: linear-gradient(145deg, #24113e, #170c2d);
    padding: 20px;
    border: 1px solid #7040a8;
    border-radius: 16px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.2);
}

div[data-testid="stMetricLabel"] {
    color: #d9baff;
}

div[data-testid="stMetricValue"] {
    color: white;
    font-weight: 800;
}

/* Tarjetas */
.vm-card {
    background: linear-gradient(145deg, #291448, #180d2e);
    border: 1px solid #8146bc;
    border-radius: 18px;
    padding: 25px;
    min-height: 125px;
    color: white;
    transition: 0.3s;
}

.vm-card:hover {
    border-color: #d36cff;
    box-shadow: 0 0 20px rgba(180, 80, 255, 0.3);
    transform: translateY(-4px);
}

.vm-card b {
    font-size: 21px;
    color: #d9a5ff;
}

.vm-card p {
    color: #eee5ff;
    font-size: 15px;
}

/* Titulos */
h2, h3 {
    color: white !important;
}

/* Fotografias */
.team-card {
    background: linear-gradient(145deg, #35145b, #170d2c);
    border: 1px solid #a34dff;
    border-radius: 20px;
    padding: 18px;
    text-align: center;
    box-shadow: 0 5px 20px rgba(120, 40, 200, 0.18);
    height: 100%;
}

.team-photo {
    width: 100%;
    max-width: 230px;
    height: 230px;
    object-fit: cover;
    object-position: center 35%;
    border-radius: 18px;
    border: 3px solid #c16aff;
    box-shadow: 0 0 22px rgba(180, 80, 255, 0.4);
}

.team-name {
    color: white;
    font-size: 19px;
    font-weight: 700;
    margin-top: 14px;
}

/* Separadores */
hr {
    border-color: #633b91 !important;
}

</style>
""", unsafe_allow_html=True)


# ---------------------------------
# LOGO Y ENCABEZADO
# ---------------------------------

logo = """
<svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="vmgrad" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#f05cff"/>
      <stop offset="100%" stop-color="#6947ff"/>
    </linearGradient>
  </defs>
  <path d="M18 55 V42 A32 32 0 0 1 82 42 V55"
        fill="none" stroke="url(#vmgrad)"
        stroke-width="8" stroke-linecap="round"/>
  <rect x="8" y="48" width="15" height="30" rx="7"
        fill="url(#vmgrad)"/>
  <rect x="77" y="48" width="15" height="30" rx="7"
        fill="url(#vmgrad)"/>
  <path d="M48 25 V68 L69 58 V15 L48 25"
        fill="url(#vmgrad)"/>
  <path d="M36 77 Q50 87 64 77"
        fill="none" stroke="#d98aff"
        stroke-width="4" stroke-linecap="round"/>
</svg>
"""

st.markdown(f"""
<div class="vm-hero">
    <div class="vm-logo">
        {logo}
        <div>
            <h1>Vibra <span>Musical</span></h1>
            <p>Explora, descubre y juega con canciones en inglés de todos los géneros.</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ---------------------------------
# ESTADISTICAS
# ---------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric("🎵 Canciones", r["canciones"])
c2.metric("🎤 Artistas", r["artistas"])
c3.metric("🎧 Géneros", r["generos"])
c4.metric("📅 Años", f'{r["anio_min"]} – {r["anio_max"]}')


# ---------------------------------
# FUNCIONES DE LA PAGINA
# ---------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("✨ ¿Qué puedes hacer aquí?")

a, b, c = st.columns(3)

with a:
    st.markdown("""
    <div class="vm-card">
        <b>🔎 Explorar</b>
        <p>Filtra canciones por género, año o artista y descubre gráficos.</p>
    </div>
    """, unsafe_allow_html=True)

with b:
    st.markdown("""
    <div class="vm-card">
        <b>🎮 Jugar</b>
        <p>Demuestra tus conocimientos adivinando el género y la década.</p>
    </div>
    """, unsafe_allow_html=True)

with c:
    st.markdown("""
    <div class="vm-card">
        <b>❤️ Mi música</b>
        <p>Organiza tus canciones favoritas y descarga tu propia lista.</p>
    </div>
    """, unsafe_allow_html=True)


# ---------------------------------
# EQUIPO
# ---------------------------------

st.markdown("<br>", unsafe_allow_html=True)
st.subheader("💜 Nuestro equipo")

integrantes = [
    ("foto_estudiante_1", "Leydy Peñates"),
    ("foto_estudiante_2", "Katherine Jaramillo"),
    ("foto_estudiante_3", "Yuliana Giraldo"),
]

cols = st.columns(3)

for col, (archivo, nombre) in zip(cols, integrantes):

    with col:
        ruta = buscar_imagen(archivo)

        if ruta:
            try:
                with open(ruta, "rb") as foto:
                    contenido = base64.b64encode(
                        foto.read()
                    ).decode()

                mime = mimetypes.guess_type(str(ruta))[0] or "image/png"

                nombre_seguro = html.escape(nombre)

                st.markdown(f"""
                <div class="team-card">
                    <img
                        class="team-photo"
                        src="data:{mime};base64,{contenido}"
                    />
                    <div class="team-name">{nombre_seguro}</div>
                </div>
                """, unsafe_allow_html=True)

            except Exception:
                st.info(f"No se pudo cargar la foto de {nombre}")

        else:
            st.info(f"Falta la foto de {nombre} en assets/")
