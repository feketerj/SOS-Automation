# UI Module

## Purpose
User interface for system interaction including web dashboard, API endpoints, and real-time updates.

## Components
- `web_server.py`: Flask/FastAPI web application
- `static/`: Frontend assets (HTML, CSS, JavaScript)
- `templates/`: Server-side templates
- `api_routes.py`: REST API endpoints
- `websocket_handler.py`: Real-time updates
- `dashboard.py`: Monitoring interface

## Architecture Reference
See [/architecture.md](/architecture.md#4-ui-module-srcui) for detailed specifications.

## Interface Types
- Web dashboard (primary)
- Command-line interface
- REST API
- WebSocket for real-time updates
- Mobile-responsive design

## Trace Points
- Records trace point: **UI Render**