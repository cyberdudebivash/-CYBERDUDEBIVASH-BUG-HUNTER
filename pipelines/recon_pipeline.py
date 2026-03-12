"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Recon Pipeline (Sentinel APEX Integrated)
Path: pipelines/recon_pipeline.py
Version: 6.0.0 (Production Hardened)

Features:
- Python 3.11+ Compatibility (redis.asyncio)
- Real-Time Sentinel APEX Intelligence Uplink
- Autonomous BOLA & Cloud Hunter Agents
"""

import asyncio
import logging
import json
import redis.asyncio as redis  # Modern replacement for aioredis
from datetime import datetime
from typing import List, Dict, Set, Any

# --- Core Component Imports ---
from subdomain_intelligence_engine import SubdomainIntelligenceEngine
from http_probe_engine import probe_hosts
from tech_fingerprinter import fingerprint_host
from javascript_endpoint_extractor import extract_js_endpoints
from database import save_asset, save_scan

# --- Enterprise Intelligence Agents ---
from agents.bola_intelligence_agent import BOLAAgent
from multi_cloud_bucket_hunter import MultiCloudBucketHunter
from intel.apex_uplink import ApexUplink  # The Sentinel APEX Bridge

# Configure elite-level logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - [CDB-PIPELINE] - %(message)s')
logger = logging.getLogger(__name__)

class ReconPipeline:
    def __init__(self, domain: str, wordlist: str, concurrency: int = 150):
        self.domain = domain
        self.wordlist = wordlist
        self.concurrency = concurrency
        
        # Internal State
        self.subdomains: List[str] = []
        self.live_hosts: List[Dict] = []
        self.api_inventory: Set[str] = set()
        self.critical_findings: List[Dict] = []
        
        # Integration Clients
        self.redis_url = "redis://localhost:6379/0"
        self.apex = ApexUplink()  # Connects to CyberDudeBivash Sentinel APEX
        self.start_time = datetime.utcnow()

    async def _publish_intelligence(self, finding: Dict[str, Any]):
        """
        Dual-Uplink Strategy:
        1. Local Redis: For the real-time Dashboard/Alert Engine.
        2. Sentinel APEX: For the global Threat Intel Platform.
        """
        finding["domain"] = self.domain
        finding["detected_at"] = datetime.utcnow().isoformat()
        
        # 1. Local Alert (Redis Pub/Sub)
        try:
            client = redis.from_url(self.redis_url)
            await client.publish("recon_alerts", json.dumps(finding))
            await client.close()
        except Exception as e:
            logger.error(f"[ALERTS-ERR] Redis publish failed: {e}")

        # 2. Sentinel APEX Sync (Enterprise Integration)
        if finding.get("severity") == "CRITICAL":
            await self.apex.push_vulnerability(finding)

    async def _phase_1_discovery(self):
        """Active & Passive Subdomain Intelligence."""
        logger.info(f"Initiating Discovery Swarm for: {self.domain}")
        engine = SubdomainIntelligenceEngine(self.domain, self.wordlist, self.concurrency)
        self.subdomains = await engine.run()

    async def _phase_2_infrastructure(self):
        """Probing & Technology Fingerprinting."""
        if not self.subdomains: return
        self.live_hosts = await probe_hosts(self.subdomains)
        
        tasks = [fingerprint_host(x["url"]) for x in self.live_hosts]
        tech_results = await asyncio.gather(*tasks)
        
        for i, entry in enumerate(self.live_hosts):
            save_asset(domain=self.domain, host=entry["url"], tech=tech_results[i])

    async def _phase_3_logic_extraction(self):
        """JavaScript Analysis & API Mapping."""
        if not self.live_hosts: return
        urls = [x["url"] for x in self.live_hosts]
        endpoints = await extract_js_endpoints(urls)
        
        for ep in endpoints:
            if any(k in ep.lower() for k in ["/api/", "/v1/", "/v2/", "/graphql"]):
                self.api_inventory.add(ep)

    async def _phase_4_autonomous_agents(self):
        """The Money Layer: BOLA & Cloud Hunting."""
        logger.info(f"Launching Agentic Security Swarm for {self.domain}...")
        
        # 1. Agentic BOLA Testing
        if self.api_inventory:
            agent = BOLAAgent(concurrency=30)
            findings = await agent.run_swarm_bola(list(self.api_inventory))
            for f in findings:
                f["type"], f["severity"] = "BOLA_VULNERABILITY", "CRITICAL"
                self.critical_findings.append(f)
                await self._publish_intelligence(f)

        # 2. Multi-Cloud Hunter
        hunter = MultiCloudBucketHunter(self.domain)
        leaks = await hunter.run_hunt()
        for leak in leaks:
            leak["type"], leak["severity"] = "CLOUD_STORAGE_LEAK", "CRITICAL"
            self.critical_findings.append(leak)
            await self._publish_intelligence(leak)

    async def run(self):
        """Orchestrate end-to-end production pipeline."""
        try:
            await self._phase_1_discovery()
            await self._phase_2_infrastructure()
            await self._phase_3_logic_extraction()
            await self._phase_4_autonomous_agents()
            
            # Persist scan results
            save_scan(self.domain, len(self.critical_findings))
            
            duration = (datetime.utcnow() - self.start_time).total_seconds()
            logger.info(f"Pipeline finished: {self.domain} in {duration:.2f}s.")
            return {"status": "SUCCESS", "critical_count": len(self.critical_findings)}
        except Exception as e:
            logger.error(f"Pipeline Failure for {self.domain}: {str(e)}")
            return {"status": "FAILED", "error": str(e)}