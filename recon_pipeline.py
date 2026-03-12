"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Recon Pipeline
Path: pipelines/recon_pipeline.py
"""
import asyncio
import logging
import json
import redis.asyncio as redis
from datetime import datetime
from typing import List, Dict, Set, Any

from subdomain_intelligence_engine import SubdomainIntelligenceEngine
from http_probe_engine import probe_hosts
from tech_fingerprinter import fingerprint_host
from javascript_endpoint_extractor import extract_js_endpoints
from database import save_asset, save_scan
from agents.bola_intelligence_agent import BOLAAgent
from multi_cloud_bucket_hunter import MultiCloudBucketHunter
from intel.apex_uplink import ApexUplink

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CDB-PIPELINE] - %(message)s')
logger = logging.getLogger(__name__)

class ReconPipeline:
    def __init__(self, domain: str, wordlist: str, concurrency: int = 150):
        self.domain = domain
        self.wordlist = wordlist
        self.concurrency = concurrency
        self.subdomains, self.live_hosts = [], []
        self.api_inventory = set()
        self.critical_findings = []
        self.apex = ApexUplink()
        self.start_time = datetime.utcnow()

    async def _publish_intelligence(self, finding: Dict[str, Any]):
        finding.update({"domain": self.domain, "detected_at": datetime.utcnow().isoformat()})
        try:
            client = redis.from_url("redis://localhost:6379/0")
            await client.publish("recon_alerts", json.dumps(finding))
            await client.close()
        except Exception as e:
            logger.error(f"Redis publish failed: {e}")

        if finding.get("severity") == "CRITICAL":
            await self.apex.push_vulnerability(finding)

    async def run(self):
        try:
            # Phase 1: Subdomain Discovery
            engine = SubdomainIntelligenceEngine(self.domain, self.wordlist, self.concurrency)
            self.subdomains = await engine.run()

            # Phase 2 & 4 in Parallel: Infrastructure & Agentic Hunting
            await asyncio.gather(
                self._phase_infrastructure(),
                self._phase_autonomous_agents()
            )
            
            save_scan(self.domain, len(self.critical_findings))
            return {"status": "SUCCESS", "critical_count": len(self.critical_findings)}
        except Exception as e:
            logger.error(f"Pipeline Failure: {e}")
            return {"status": "FAILED", "error": str(e)}

    async def _phase_infrastructure(self):
        if not self.subdomains: return
        self.live_hosts = await probe_hosts(self.subdomains)
        for host in self.live_hosts:
            tech = await fingerprint_host(host["url"])
            save_asset(self.domain, host["url"], tech)

    async def _phase_autonomous_agents(self):
        # Cloud Hunting and BOLA integration
        hunter = MultiCloudBucketHunter(self.domain)
        leaks = await hunter.run_hunt()
        for leak in leaks:
            leak["severity"] = "CRITICAL"
            await self._publish_intelligence(leak)