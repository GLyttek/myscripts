# Debian Monitoring App

This project provides a minimal FastAPI backend and React-based frontend for realtime system monitoring on Debian. It integrates with the Ollama API using the `phi4.1:latest` model to interpret metrics.

## Backend

- Python FastAPI server (`backend/main.py`)
- Uses WebSocket to stream metrics.
- JWT-based login with configurable credentials via `.env`.
- Example metrics gathered from `psutil`.
- Ollama integration via `analyze_with_ollama()` which calls the REST API.

### Running

Install dependencies and start:

```bash
cd backend
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Frontend

`frontend/index.html` is a simple React dashboard using CDN libraries. Open the file in a browser once the backend is running to see metrics and analysis results.

## Security Notes

- Change `SECRET_KEY`, `ADMIN_USER`, and `ADMIN_PASS` in `.env`.
- Use HTTPS termination in production.

This is a starting point for a full-featured monitoring solution.
