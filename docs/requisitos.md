# Requisitos — Vibra Musical

## Requisitos funcionales
| ID | Requisito |
|----|-----------|
| RF1 | La app muestra una página de inicio con métricas del catálogo (canciones, artistas, géneros, años). |
| RF2 | El usuario puede filtrar canciones por género, rango de años y texto (título/artista). |
| RF3 | La app muestra gráficos por género, década y artista. |
| RF4 | La app incluye un juego de 10 preguntas (adivinar género o década) con puntaje. |
| RF5 | El usuario puede armar una lista de favoritas, agregar canciones propias y descargarla en CSV. |
| RF6 | La app muestra información básica de los datos (filas, columnas, nulos). |

## Requisitos no funcionales
| ID | Requisito |
|----|-----------|
| RNF1 | Funciona con Python 3 y Streamlit; dependencias en `requirements.txt`. |
| RNF2 | Los datos se cargan desde `data/datos.csv` con caché para rendimiento. |
| RNF3 | Interfaz con tema oscuro y estilos propios en `assets/estilos.css`. |
| RNF4 | El código está versionado en GitHub (ver `plan_versionado.md`). |

## Datos
- Fuente: lista de 139 canciones en inglés de 17 géneros (1954–2023) con título, artista, género y año.
- Limpieza documentada en `data/limpieza.ipynb`.
