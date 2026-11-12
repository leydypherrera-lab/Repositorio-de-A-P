# Manual de usuario — Vibra Musical

## Cómo abrir la app
1. Abre la terminal en la carpeta del proyecto.
2. Activa el entorno: `.venv\Scripts\activate` (Windows).
3. Ejecuta: `streamlit run app.py`
4. Se abre el navegador en http://localhost:8501

## Páginas
- **Inicio:** resumen del catálogo y el equipo.
- **Explorar:** usa los filtros de la barra lateral (género, años, búsqueda). Cambia entre la tabla y los gráficos con las pestañas.
- **Jugar:** elige el modo (género o década), pulsa *Empezar* y responde 10 preguntas. Al final verás tu puntaje.
- **Mis datos:** elige favoritas del catálogo, agrega canciones propias en el formulario y descarga tu lista en CSV.

## Problemas comunes
| Problema | Solución |
|----------|----------|
| `streamlit` no se reconoce | Activa el entorno virtual e instala con `pip install -r requirements.txt`. |
| No aparece la foto del equipo | Revisa que el archivo esté en `assets/` con el nombre `foto_estudiante_1.png`. |
| La página no cambia al guardar | Pulsa *Rerun* o activa *Always rerun* en la esquina superior derecha. |
