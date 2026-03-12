"""
SENTINEL APEX UPLINK - Production Intelligence Synchronization
Path: intel/apex_uplink.py
"""

import aiohttp
import logging
import hashlib
from datetime import datetime
from config import settings

logger = logging.getLogger(__name__)

class ApexUplink:
    def __init__(self):
        self.api_url = "https://api.sentinel-apex.com/v1/intel/ingest"
        self.api_key = settings.SENTINEL_APEX_KEY
        self.sync_cache = set()

    async def push_vulnerability(self, finding: dict):
        """Pushes findings with unique deduplication logic."""
        # Generate hash to prevent duplicate syncing
        finding_id = hashlib.sha256(f"{finding['type']}{finding.get('url','')}".encode()).hexdigest()
        
        if finding_id in self.sync_cache:
            return

        payload = {
            "source": "CDB_BUG_HUNTER_SWARM",
            "type": finding.get("type"),
            "severity": finding.get("severity", "CRITICAL"),
            "target": finding.get("url") or finding.get("bucket"),
            "detected_at": datetime.utcnow().isoformat()
        }
        
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.api_url, json=payload, headers=headers) as resp:
                    if resp.status == 201:
                        self.sync_cache.add(finding_id)
                        logger.info(f"[APEX] Intelligence synced for {finding.get('domain')}")
            except Exception as e:
                logger.error(f"[APEX] Uplink error: {e}")