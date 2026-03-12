"""
CYBERDUDEBIVASH - God-Mode API & WebSocket Server
Path: dashboard/backend/api_server.py
"""

import asyncio
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import redis.asyncio as redis
from config import settings
from analytics.roi_calculator import ROICalculator

# --- 1. Initialize High-Authority Logger ---
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CDB-API] - %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI(title="CyberDudeBivash God-Mode API")
roi_engine = ROICalculator()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

@app.on_event("startup")
async def startup_event():
    # Starts the background Redis listener
    asyncio.create_task(redis_listener())

async def redis_listener():
    """
    Listens to the 'recon_alerts' channel and broadcasts to the GUI.
    """
    r = redis.from_url(settings.REDIS_URL, decode_responses=True)
    pubsub = r.pubsub()
    await pubsub.subscribe("recon_alerts")
    
    # FIX: Logger is now correctly defined above
    logger.info("[WS-BRIDGE] Real-time swarm listener active.")
    
    async for message in pubsub.listen():
        if message["type"] == "message":
            data = json.loads(message["data"])
            
            if data.get("severity") == "CRITICAL":
                roi_stats = roi_engine.calculate_risk_exposure([data])
                data["roi_metrics"] = roi_stats
            
            await manager.broadcast(json.dumps(data))

@app.websocket("/ws/swarm")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)