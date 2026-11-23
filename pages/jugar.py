from datetime import datetime
import random

import streamlit as st

from src.data import cargar_datos

st.title("🎮 Jugar")
df = cargar_datos()

N_PREGUNTAS = 10

# Inicializar historial permanente en la sesión si no existe
if "historial_juegos" not in st.session_state:
    st.session_state["historial_juegos"] = []


def mostrar_flores_flotantes():
    """Inyecta una animación CSS de flores flotando por toda la pantalla."""
    flores = ["🌸", "🌺", "🌼", "🌷", "🌻", "💐", "💮"]
    elementos_html = ""
    for i in range(35):
        flor = random.choice(flores)
        izquierda = random.randint(0, 98)
        duracion = round(random.uniform(3.5, 7.0), 2)
        retraso = round(random.uniform(0.0, 2.5), 2)
        tamano = random.randint(24, 42)
        elementos_html += (
            f'<div class="vm-flor" style="left:{izquierda}vw; '
            f'animation-duration:{duracion}s; animation-delay:{retraso}s; '
            f'font-size:{tamano}px;">{flor}</div>'
        )

    st.markdown(
        f"""
        <style>
        @keyframes flotarFlores {{
            0% {{
                transform: translateY(105vh) rotate(0deg) scale(0.8);
                opacity: 0;
            }}
            15% {{
                opacity: 1;
            }}
            85% {{
                opacity: 1;
            }}
            100% {{
                transform: translateY(-15vh) rotate(360deg) scale(1.1);
                opacity: 0;
            }}
        }}
        .vm-flor {{
            position: fixed;
            bottom: -50px;
            z-index: 999999;
            pointer-events: none;
            user-select: none;
            animation-name: flotarFlores;
            animation-timing-function: ease-in-out;
            animation-fill-mode: forwards;
        }}
        </style>
        {elementos_html}
        """,
        unsafe_allow_html=True,
    )


def nueva_partida(modo: str):
    campo = "genero" if modo == "Adivina el género" else "decada"
    muestra = df.sample(N_PREGUNTAS)
    opciones_total = sorted(df[campo].unique())
    preguntas = []
    for _, fila in muestra.iterrows():
        correcta = fila[campo]
        otras = [o for o in opciones_total if o != correcta]
        opciones = random.sample(otras, 3) + [correcta]
        random.shuffle(opciones)
        preguntas.append(
            {
                "titulo": fila["titulo"],
                "artista": fila["artista"],
                "correcta": correcta,
                "opciones": opciones,
            }
        )
    st.session_state.juego = {
        "modo": modo,
        "preguntas": preguntas,
        "i": 0,
        "puntos": 0,
        "respondida": False,
        "acierto": None,
        "guardada": False,
    }


def responder():
    j = st.session_state.juego
    p = j["preguntas"][j["i"]]
    eleccion = st.session_state.get(f"resp_{j['i']}")
    j["acierto"] = eleccion == p["correcta"]
    j["puntos"] += int(j["acierto"])
    j["respondida"] = True


def siguiente():
    j = st.session_state.juego
    j["i"] += 1
    j["respondida"] = False
    j["acierto"] = None


def terminar():
    st.session_state.pop("juego", None)


# ---------- Pantalla de inicio ----------
if "juego" not in st.session_state:
    st.write(f"Responde {N_PREGUNTAS} preguntas sobre canciones. ¡Mira cuánto sabes!")
    modo = st.radio("Modo de juego", ["Adivina el género", "Adivina la década"], horizontal=True)
    st.button("Empezar 🚀", type="primary", on_click=nueva_partida, args=(modo,))

    # Mostrar resumen de progreso guardado si ya jugó antes
    historial = st.session_state["historial_juegos"]
    if historial:
        st.divider()
        st.subheader("🏆 Tu progreso guardado")
        c1, c2, c3 = st.columns(3)
        c1.metric("Partidas jugadas", len(historial))
        c2.metric("Mejor puntaje", f"{max(h['puntos'] for h in historial)} / {N_PREGUNTAS}")
        c3.metric("Victorias (8+ pts)", sum(1 for h in historial if h["gano"]))

        with st.expander("Ver historial de partidas"):
            for h in reversed(historial):
                estado = "🌸 ¡Ganada!" if h["gano"] else "🎧 Completada"
                st.write(f"**{h['fecha']}** · {h['modo']} — **{h['puntos']}/{N_PREGUNTAS}** ({estado})")
    st.stop()

j = st.session_state.juego

# ---------- Resultado final ----------
if j["i"] >= N_PREGUNTAS:
    gano = j["puntos"] >= 8

    # Guardar la partida en el historial una sola vez
    if not j.get("guardada"):
        st.session_state["historial_juegos"].append(
            {
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "modo": j["modo"],
                "puntos": j["puntos"],
                "total": N_PREGUNTAS,
                "gano": gano,
            }
        )
        j["guardada"] = True

    st.header(f"Puntaje final: {j['puntos']} / {N_PREGUNTAS}")
    if gano:
        mostrar_flores_flotantes()
        st.success("🌸 ¡Felicidades, ganaste! Eres un experto musical.")
    elif j["puntos"] >= 5:
        st.info("¡Buen trabajo! Sigue practicando para ganar flores.")
    else:
        st.warning("Hay que escuchar más música 🎧")

    st.button("Jugar de nuevo", type="primary", on_click=terminar)
    st.stop()

# ---------- Pregunta actual ----------
p = j["preguntas"][j["i"]]
st.progress(j["i"] / N_PREGUNTAS, text=f"Pregunta {j['i'] + 1} de {N_PREGUNTAS} · Puntos: {j['puntos']}")

pide = "el GÉNERO" if j["modo"] == "Adivina el género" else "la DÉCADA"
st.markdown(
    f'<div class="vm-pregunta">¿Cuál es {pide} de “{p["titulo"]}” de {p["artista"]}?</div>',
    unsafe_allow_html=True,
)

st.radio("Elige una opción", p["opciones"], key=f"resp_{j['i']}", disabled=j["respondida"])

if not j["respondida"]:
    st.button("Responder", type="primary", on_click=responder)
else:
    if j["acierto"]:
        st.markdown('<span class="vm-ok">✅ ¡Correcto!</span>', unsafe_allow_html=True)
    else:
        st.markdown(f'<span class="vm-mal">❌ Era: {p["correcta"]}</span>', unsafe_allow_html=True)
    etiqueta = "Siguiente ➡️" if j["i"] < N_PREGUNTAS - 1 else "Ver resultado 🏁"
    st.button(etiqueta, type="primary", on_click=siguiente)