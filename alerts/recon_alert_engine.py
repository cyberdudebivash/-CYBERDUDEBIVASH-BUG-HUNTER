"""
CYBERDUDEBIVASH BUG HUNTER - Real-Time Alert Engine
Path: alerts/recon_alert_engine.py
Purpose: Instant notification delivery for Critical findings.
"""

import asyncio
import aioredis
import json
import aiohttp
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from typing import List

app = FastAPI()

# Configuration (In production, move to config.py)
REDIS_URL = "redis://localhost:6379/0"
DISCORD_WEBHOOK = "https://discord.com/api/webhooks/YOUR_WEBHOOK"
TELEGRAM_BOT_TOKEN = "YOUR_BOT_TOKEN"
TELEGRAM_CHAT_ID = "YOUR_CHAT_ID"

class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except:
                pass

manager = ConnectionManager()

async def send_external_alerts(finding: dict):
    """Dispatches alerts to Discord and Telegram."""
    message = (
        f"🚨 **CRITICAL FINDING DISCOVERED** 🚨\n"
        f"**Type:** {finding.get('type', 'Unknown')}\n"
        f"**Target:** {finding.get('domain')}\n"
        f"**Evidence:** {finding.get('url') or finding.get('bucket')}\n"
        f"**Severity:** CRITICAL"
    )

    async with aiohttp.ClientSession() as session:
        # 1. Discord
        try:
            await session.post(DISCORD_WEBHOOK, json={"content": message})
        except Exception as e:
            print(f"Discord Alert Failed: {e}")

        # 2. Telegram
        try:
            tg_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            await session.post(tg_url, json={"chat_id": TELEGRAM_CHAT_ID, "text": message})
        except Exception as e:
            print(f"Telegram Alert Failed: {e}")

async def redis_listener():
    """Listens for new findings published by the recon pipeline."""
    redis = await aioredis.from_url(REDIS_URL, decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe("recon_alerts")

    print("[Alerts] Listening for live findings...")
    async for message in pubsub.listen():
        if message["type"] == "message":
            finding = json.loads(message["data"])
            # Broadcast to UI
            await manager.broadcast(json.dumps(finding))
            # Send to External Webhooks
            await send_external_alerts(finding)

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(redis_listener())

@app.websocket("/ws/alerts")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket)