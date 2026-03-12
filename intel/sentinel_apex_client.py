"""
SENTINEL APEX CLIENT - Unified Intelligence & Reasoning Interface
Path: intel/sentinel_apex_client.py
Version: 3.0.0 (God-Mode Synchronized)
"""

import aiohttp
import json
import logging
import hashlib
import hmac
from datetime import datetime
from typing import Dict, Any, Optional
from config import settings

logger = logging.getLogger(__name__)

class SentinelAIClient:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or settings.SENTINEL_APEX_KEY
        self.signing_key = settings.APEX_SECRET_SIGNING_KEY
        self.base_url = settings.SENTINEL_APEX_URL

    def _generate_signature(self, payload: str) -> str:
        """Generates an HMAC signature to prove identity to the APEX core."""
        return hmac.new(
            self.signing_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

    async def get_reasoning(self, prompt: str) -> Dict[str, Any]:
        """Connects to the Sentinel APEX LLM Engine for God-Mode strategy."""
        endpoint = f"{self.base_url}/ai/reasoning"
        payload = {"prompt": prompt, "model": "cyberdude-brain-v2-ultra"}
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(endpoint, json=payload, headers=headers, timeout=15) as resp:
                    if resp.status == 200:
                        return await resp.json()
                    return {"priority": 0, "summary": "Offline", "next_steps": []}
            except Exception as e:
                logger.error(f"[AI-REASONING] Connection to Sentinel APEX Brain failed: {e}")
                return {"priority": 0, "summary": "Error", "next_steps": []}

    async def push_vulnerability(self, finding: Dict[str, Any]) -> bool:
        """Synchronizes a critical finding to the Sentinel APEX Global Threat Feed."""
        endpoint = f"{self.base_url}/intel/ingest"
        telemetry = {
            "source": "CDB_BUG_HUNTER_SWARM",
            "type": finding.get("type"),
            "severity": finding.get("severity", "CRITICAL"),
            "target": finding.get("domain"),
            "evidence": finding.get("url") or finding.get("bucket"),
            "metadata": finding,
            "detected_at": datetime.utcnow().isoformat()
        }
        payload_str = json.dumps(telemetry)
        headers = {
            "Content-Type": "application/json",
            "X-Sentinel-Key": self.api_key,
            "X-Sentinel-Signature": self._generate_signature(payload_str)
        }
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(endpoint, data=payload_str, headers=headers) as resp:
                    return resp.status in [200, 201]
            except Exception as e:
                logger.error(f"[INTEL-SYNC] Connection error: {e}")
                return False