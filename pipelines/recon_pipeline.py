"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Recon Pipeline (Sentinel APEX Integrated)
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
from config import settings

logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CDB-PIPELINE] - %(message)s')
logger = logging.getLogger(__name__)

class ReconPipeline:
    def __init__(self, domain: str, wordlist: str, concurrency: int = 150):
        self.domain = domain
        self.wordlist = wordlist
        self.concurrency = concurrency
        self.subdomains: List[str] = []
        self.live_hosts: List[Dict] = []
        self.api_inventory: Set[str] = set()
        self.critical_findings: List[Dict] = []
        self.apex = ApexUplink()
        self.start_time = datetime.utcnow()

    async def _publish_intelligence(self, finding: Dict[str, Any]):
        """Dual-Uplink Strategy for Local Dashboard and Sentinel APEX Brain."""
        finding["domain"] = self.domain
        finding["detected_at"] = datetime.utcnow().isoformat()
        
        try:
            client = redis.from_url(settings.REDIS_URL)
            await client.publish("recon_alerts", json.dumps(finding))
            await client.close()
        except Exception as e:
            logger.error(f"[ALERTS-ERR] Redis publish failed: {e}")

        if finding.get("severity") == "CRITICAL":
            await self.apex.push_vulnerability(finding)

    async def _phase_infrastructure(self):
        """Processes tech stack and assets in parallel."""
        if not self.subdomains: return
        self.live_hosts = await probe_hosts(self.subdomains)
        tasks = [fingerprint_host(x["url"]) for x in self.live_hosts]
        tech_results = await asyncio.gather(*tasks)
        for i, entry in enumerate(self.live_hosts):
            save_asset(domain=self.domain, host=entry["url"], tech=tech_results[i])

    async def _phase_autonomous_agents(self):
        """Agentic BOLA and Cloud Hunting."""
        hunter = MultiCloudBucketHunter(self.domain)
        leaks = await hunter.run_hunt()
        for leak in leaks:
            leak["severity"] = "CRITICAL"
            self.critical_findings.append(leak)
            await self._publish_intelligence(leak)

        if self.api_inventory:
            agent = BOLAAgent(concurrency=30)
            findings = await agent.run_swarm_bola(list(self.api_inventory))
            for f in findings:
                f["severity"] = "CRITICAL"
                self.critical_findings.append(f)
                await self._publish_intelligence(f)

    async def run(self):
        try:
            # Phase 1: Subdomain Intelligence
            engine = SubdomainIntelligenceEngine(self.domain, self.wordlist, self.concurrency)
            self.subdomains = await engine.run()

            # Phase 2 & 4 in Parallel: Infrastructure Probing & Agentic Hunting
            await asyncio.gather(
                self._phase_infrastructure(),
                self._phase_autonomous_agents()
            )

            save_scan(self.domain, len(self.critical_findings))
            return {"status": "SUCCESS", "critical_count": len(self.critical_findings)}
        except Exception as e:
            logger.error(f"Pipeline Failure for {self.domain}: {str(e)}")
            return {"status": "FAILED", "error": str(e)}