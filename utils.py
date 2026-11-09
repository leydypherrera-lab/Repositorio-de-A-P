import ast
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).parent
DATA_PATH = BASE_DIR / "data" / "final_dataset_V4-selected-columns.csv"
ASSETS = BASE_DIR / "assets"

FEATURES = ["acousticness", "danceability", "energy", "instrumentalness"]


def _parsear_generos(valor):
    if pd.isna(valor):
        return []
    texto = str(valor).strip()
    try:
        data = ast.literal_eval(texto)
        if isinstance(data, (list, tuple)):
            return [str(g).strip().lower() for g in data if str(g).strip()]
    except (ValueError, SyntaxError):
        pass
    return [g.strip().lower() for g in texto.split(",") if g.strip()]


@st.cache_data
def cargar_datos():
    df = pd.read_csv(DATA_PATH)

    df = df.dropna(subset=["artist_name", "song_name"])
    df = df.drop_duplicates(subset=["artist_name", "song_name"])
    df["artist_name"] = df["artist_name"].astype(str).str.strip()
    df["song_name"] = df["song_name"].astype(str).str.strip()
    df["language"] = df["language"].fillna("desconocido").astype(str).str.strip()
    df["lyrics"] = df["lyrics"].fillna("Letra no disponible")

    for col in FEATURES:
        df[col] = pd.to_numeric(df[col], errors="coerce").clip(0, 1)
    df["new_artist_popularity"] = pd.to_numeric(
        df["new_artist_popularity"], errors="coerce"
    ).clip(0, 100)
    df = df.dropna(subset=FEATURES + ["new_artist_popularity"])

    df["genres_list"] = df["genres"].apply(_parsear_generos)
    df["genres_txt"] = df["genres_list"].apply(", ".join)
    return df.reset_index(drop=True)


def mostrar_imagen(ruta, **kwargs):
    if Path(ruta).exists():
        st.image(str(ruta), **kwargs)
    else:
        st.info(f"Falta la imagen: {Path(ruta).name}")


def inicializar_estado():
    if "favoritos" not in st.session_state:
        st.session_state["favoritos"] = []