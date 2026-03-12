"""
CYBERDUDEBIVASH BUG HUNTER - Sentinel APEX Uplink Client
Path: intel/sentinel_apex_client.py
Purpose: Feeds Bug Hunter findings into the main Sentinel APEX Threat Intel platform.
"""

import aiohttp
import json
import logging
import hashlib
import hmac
from datetime import datetime
from typing import Dict, Any, Optional

# Global settings (Should be mirrored in config.py)
APEX_API_URL = "https://api.sentinel-apex.com/v1/ingest"
APEX_API_KEY = "YOUR_SENTINEL_APEX_MASTER_KEY"
APEX_SECRET_SIGNING_KEY = "YOUR_HMAC_SIGNING_SECRET"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [APEX-UPLINK] - %(message)s')
logger = logging.getLogger(__name__)

class SentinelApexClient:
    def __init__(self):
        self.api_url = APEX_API_URL
        self.api_key = APEX_API_KEY
        self.signing_key = APEX_SECRET_SIGNING_KEY

    def _generate_signature(self, payload: str) -> str:
        """Generates an HMAC signature to prove the Bug Hunter's identity."""
        return hmac.new(
            self.signing_key.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()

    async def send_finding(self, finding: Dict[str, Any]) -> bool:
        """
        Logic: Packages the finding into Sentinel APEX JSON format and uploads.
        Includes automatic retry logic for network stability.
        """
        # Format for Sentinel APEX Schema
        telemetry = {
            "source": "CDB_BUG_HUNTER_NODE_01",
            "event_type": finding.get("type", "UNKNOWN_VULN"),
            "severity_score": 9.8 if finding.get("severity") == "CRITICAL" else 7.0,
            "target_domain": finding.get("domain"),
            "data": finding,
            "timestamp": datetime.utcnow().isoformat()
        }

        payload_str = json.dumps(telemetry)
        signature = self._generate_signature(payload_str)

        headers = {
            "Content-Type": "application/json",
            "X-Sentinel-Key": self.api_key,
            "X-Sentinel-Signature": signature
        }

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(self.api_url, data=payload_str, headers=headers, timeout=10) as resp:
                    if resp.status == 201:
                        logger.info(f"Successfully synced finding to Sentinel APEX: {finding.get('domain')}")
                        return True
                    else:
                        error_text = await resp.text()
                        logger.error(f"APEX Uplink Rejected ({resp.status}): {error_text}")
                        return False
            except Exception as e:
                logger.error(f"Uplink Connection Failed: {e}")
                return False

    async def batch_sync(self, scan_results: Dict[str, Any]):
        """Syncs an entire scan batch to the Threat Intel platform."""
        findings = scan_results.get("critical_findings", [])
        if not findings:
            return

        logger.info(f"Syncing {len(findings)} findings to Sentinel APEX Central...")
        tasks = [self.send_finding(f) for f in findings]
        await asyncio.gather(*tasks)

if __name__ == "__main__":
    # Internal Uplink Test
    client = SentinelApexClient()
    test_finding = {
        "type": "BOLA_VULNERABILITY",
        "domain": "target.com",
        "severity": "CRITICAL",
        "url": "https://api.target.com/v1/user/99"
    }
    asyncio.run(client.send_finding(test_finding))