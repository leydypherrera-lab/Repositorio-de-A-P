# Plan de versionado — Vibra Musical

## Herramientas
Git + GitHub, trabajando desde VS Code.

## Ramas
- `main`: versión estable, lo que se entrega.
- `desarrollo` (opcional): cambios en curso antes de pasar a `main`.

## Reglas de commits
Mensajes cortos en español, en infinitivo y con prefijo:
- `feat:` nueva funcionalidad — `feat: agregar página jugar`
- `fix:` corrección — `fix: corregir filtro por años`
- `docs:` documentación — `docs: actualizar manual de usuario`
- `data:` cambios en datos — `data: agregar canciones de jazz`

## Versiones (etiquetas)
- `v0.1` estructura y datos
- `v0.2` páginas explorar e inicio
- `v0.3` juego y mis datos
- `v1.0` entrega final

## Flujo de trabajo
1. `git pull` antes de empezar.
2. Hacer cambios y probarlos con `streamlit run app.py`.
3. `git add .` → `git commit -m "mensaje"` → `git push`.
