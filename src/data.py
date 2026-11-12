"""Funciones de datos de Vibra Musical (carga, filtros y estadísticas)."""
from pathlib import Path

import pandas as pd
import streamlit as st

RAIZ = Path(__file__).resolve().parent.parent
RUTA_DATOS = RAIZ / "data" / "datos.csv"
RUTA_ASSETS = RAIZ / "assets"


@st.cache_data
def cargar_datos() -> pd.DataFrame:
    """Lee data/datos.csv una sola vez y lo guarda en caché."""
    return pd.read_csv(RUTA_DATOS, encoding="utf-8")


def filtrar(df, generos=None, rango_anios=None, texto=""):
    """Filtra por géneros, rango de años y texto (título o artista)."""
    res = df
    if generos:
        res = res[res["genero"].isin(generos)]
    if rango_anios:
        res = res[res["anio"].between(rango_anios[0], rango_anios[1])]
    if texto:
        t = texto.strip().lower()
        res = res[
            res["titulo"].str.lower().str.contains(t, regex=False)
            | res["artista"].str.lower().str.contains(t, regex=False)
        ]
    return res


def resumen(df) -> dict:
    """Números clave para mostrar en métricas."""
    return {
        "canciones": len(df),
        "artistas": df["artista"].nunique(),
        "generos": df["genero"].nunique(),
        "anio_min": int(df["anio"].min()),
        "anio_max": int(df["anio"].max()),
    }


def buscar_imagen(nombre_base: str):
    """Busca assets/<nombre_base>.(png|jpg|jpeg|webp); devuelve la ruta o None."""
    for ext in ("png", "jpg", "jpeg", "webp"):
        ruta = RUTA_ASSETS / f"{nombre_base}.{ext}"
        if ruta.exists():
            return str(ruta)
    return None
