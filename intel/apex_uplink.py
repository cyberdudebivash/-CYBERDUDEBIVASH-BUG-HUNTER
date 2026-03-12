"""
SENTINEL APEX UPLINK - Intelligence Synchronization
Path: intel/apex_uplink.py
Purpose: Feeds Bug Hunter findings into the Sentinel APEX ecosystem.
"""

import aiohttp
import logging
from datetime import datetime
from config import settings # Assumes APEX_API_KEY is in your .env

logger = logging.getLogger(__name__)

class ApexUplink:
    def __init__(self):
        self.api_url = "https://api.sentinel-apex.com/v1/intel/ingest"
        self.api_key = settings.SENTINEL_APEX_KEY

    async def push_vulnerability(self, finding: dict):
        """Pushes a critical finding to the APEX brain."""
        payload = {
            "source": "CDB_BUG_HUNTER_SWARM",
            "type": finding.get("type"),
            "severity": finding.get("severity"),
            "target": finding.get("url"),
            "metadata": finding,
            "detected_at": datetime.utcnow().isoformat()
        }
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.api_url, json=payload, headers=headers) as resp:
                    if resp.status == 201:
                        logger.info(f"[APEX] Successfully synced finding for {finding.get('domain')}")
                    else:
                        logger.warning(f"[APEX] Sync failed with status: {resp.status}")
            except Exception as e:
                logger.error(f"[APEX] Connection error: {e}")