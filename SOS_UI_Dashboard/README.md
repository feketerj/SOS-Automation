# SOS UI Dashboard Assets

- `web/` holds editable source files (`index.html`, `app.js`, `styles.css`).
- `dist/` contains the static files served by the FastAPI app. Rebuild with:
  ```bash
  python SOS_UI_Dashboard/build_static.py
  ```
- `UI_ARCHITECTURE.md` documents the end-to-end UX/architecture plan.

The dashboard expects the backend service (`python -m ui_service`) to be running.
