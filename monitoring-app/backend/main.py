import os
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict

import psutil
import jwt
import requests
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from starlette.websockets import WebSocketState
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "change_this_secret")
JWT_ALGORITHM = "HS256"
TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Debian Monitoring App")

# Simple CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

security = HTTPBearer()


def create_access_token(data: Dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=JWT_ALGORITHM)


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail="Invalid token") from e
    return payload


@app.post("/api/login")
async def login(username: str, password: str):
    # Replace with real authentication logic
    if username == os.getenv("ADMIN_USER", "admin") and password == os.getenv("ADMIN_PASS", "password"):
        token = create_access_token({"sub": username})
        return {"access_token": token}
    raise HTTPException(status_code=401, detail="Incorrect credentials")


def gather_metrics() -> Dict:
    return {
        "cpu": psutil.cpu_percent(interval=None),
        "memory": psutil.virtual_memory()._asdict(),
        "swap": psutil.swap_memory()._asdict(),
        "disk": psutil.disk_usage("/")._asdict(),
        "net": psutil.net_io_counters()._asdict(),
        "processes": len(psutil.pids()),
    }


async def analyze_with_ollama(metrics: Dict) -> Dict:
    """Send metrics to the Ollama REST API using phi4.1 model."""
    url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    payload = {
        "model": "phi4.1:latest",
        "prompt": json.dumps(metrics),
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        return {"error": "Failed to contact Ollama API"}


@app.get("/api/metrics")
async def get_metrics(user=Depends(verify_token)):
    metrics = gather_metrics()
    return {"metrics": metrics}


@app.websocket("/ws/metrics")
async def websocket_metrics(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            metrics = gather_metrics()
            analysis = await analyze_with_ollama(metrics)
            data = {"metrics": metrics, "analysis": analysis}
            await ws.send_text(json.dumps(data))
            await asyncio.sleep(2)
    except WebSocketDisconnect:
        if ws.application_state != WebSocketState.DISCONNECTED:
            await ws.close()


@app.get("/api/analysis")
async def get_analysis(user=Depends(verify_token)):
    metrics = gather_metrics()
    analysis = await analyze_with_ollama(metrics)
    return {"analysis": analysis}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
