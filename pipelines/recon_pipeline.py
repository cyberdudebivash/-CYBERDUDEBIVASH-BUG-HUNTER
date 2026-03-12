"""
CYBERDUDEBIVASH BUG HUNTER - Enterprise Recon Pipeline (Sentinel APEX & God-Mode Integrated)
Path: pipelines/recon_pipeline.py
Version: 9.0.0 (God-Mode Production)
"""

import asyncio
import logging
import json
import redis.asyncio as redis
from datetime import datetime
from typing import List, Dict, Set, Any

# --- Core Component Imports ---
from subdomain_intelligence_engine import SubdomainIntelligenceEngine
from http_probe_engine import probe_hosts
from tech_fingerprinter import fingerprint_host
from javascript_endpoint_extractor import extract_js_endpoints
from database import save_asset, save_scan

# --- Enterprise Intelligence & AI Agents ---
from agents.bola_intelligence_agent import BOLAAgent
from multi_cloud_bucket_hunter import MultiCloudBucketHunter
from intel.sentinel_apex_client import SentinelAIClient
from config import settings

# Configure elite-level production logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - [CDB-PIPELINE] - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class ReconPipeline:
    def __init__(self, domain: str, wordlist: str, concurrency: int = 150):
        self.domain = domain
        self.wordlist = wordlist
        self.concurrency = concurrency
        
        # Internal State Management
        self.subdomains: List[str] = []
        self.live_hosts: List[Dict] = []
        self.api_inventory: Set[str] = set()
        self.critical_findings: List[Dict] = []
        
        # Integration Clients
        self.apex = SentinelAIClient()
        self.start_time = datetime.utcnow()

    async def _publish_intelligence(self, finding: Dict[str, Any]):
        """
        Dual-Uplink Strategy:
        1. Local Dashboard: Immediate real-time alerts via Redis.
        2. AI Reasoning: God-Mode analysis for autonomous pivoting.
        3. Sentinel APEX: Global threat synchronization.
        """
        finding["domain"] = self.domain
        finding["detected_at"] = datetime.utcnow().isoformat()
        
        # 1. Real-Time Redis Alert for Dashboard
        try:
            client = redis.from_url(settings.REDIS_URL)
            await client.publish("recon_alerts", json.dumps(finding))
            await client.close()
        except Exception as e:
            logger.error(f"[ALERTS-ERR] Redis publish failed: {e}")

        # 2. God-Mode AI Analysis (Strategic Pivoting)
        # We use a local import to break circular dependency with reasoning_orchestrator
        if settings.GOD_MODE_ENABLED:
            from core.reasoning_orchestrator import orchestrator
            await orchestrator.analyze_and_retask(finding)

        # 3. Sentinel APEX Deduplicated Sync
        if finding.get("severity") == "CRITICAL":
            await self.apex.push_vulnerability(finding)

    async def _phase_infrastructure(self):
        """Processes tech stack and assets in parallel across all subdomains."""
        if not self.subdomains:
            return
            
        # Probe for live web services
        self.live_hosts = await probe_hosts(self.subdomains)
        
        # Parallel tech fingerprinting using asyncio.gather
        tasks = [fingerprint_host(x["url"]) for x in self.live_hosts]
        tech_results = await asyncio.gather(*tasks)
        
        for i, entry in enumerate(self.live_hosts):
            save_asset(domain=self.domain, host=entry["url"], tech=tech_results[i])
            
        # Extract API endpoints for subsequent BOLA testing
        urls = [x["url"] for x in self.live_hosts]
        endpoints = await extract_js_endpoints(urls)
        for ep in endpoints:
            # Filter for high-value API patterns
            if any(k in ep.lower() for k in ["/api/", "/v1/", "/v2/", "/graphql"]):
                self.api_inventory.add(ep)

    async def _phase_autonomous_agents(self):
        """The Revenue Layer: Simultaneous BOLA and Cloud Hunting Swarm."""
        logger.info(f"Launching Agentic Security Swarm for {self.domain}...")
        
        hunt_tasks = []

        # Task 1: Multi-Cloud Bucket Hunter (Leaked S3/Azure/GCP)
        hunter = MultiCloudBucketHunter(self.domain)
        hunt_tasks.append(hunter.run_hunt())

        # Task 2: Agentic BOLA Testing (API Logic Vulnerabilities)
        if self.api_inventory:
            agent = BOLAAgent(concurrency=30)
            hunt_tasks.append(agent.run_swarm_bola(list(self.api_inventory)))

        # Execute Hunting Swarm in Parallel for God-Mode Speed
        swarm_results = await asyncio.gather(*hunt_tasks)

        # Process and publish critical findings
        for result_set in swarm_results:
            if isinstance(result_set, list):
                for finding in result_set:
                    finding["severity"] = "CRITICAL"
                    self.critical_findings.append(finding)
                    await self._publish_intelligence(finding)

    async def run(self):
        """Orchestrates the full God-Mode pipeline execution."""
        try:
            logger.info(f"Initiating God-Mode Recon Pipeline for: {self.domain}")
            
            # Step 1: Subdomain Discovery (Sequential Foundation)
            engine = SubdomainIntelligenceEngine(self.domain, self.wordlist, self.concurrency)
            self.subdomains = await engine.run()

            # Step 2 & 3: Parallelized Infrastructure & Agentic Hunting Swarm
            # Findings from 'autonomous_agents' trigger 'reasoning_orchestrator'
            # to inject new tasks back into the global swarm in real-time.
            await asyncio.gather(
                self._phase_infrastructure(),
                self._phase_autonomous_agents()
            )

            # Finalize Scan Persistence
            save_scan(self.domain, len(self.critical_findings))
            
            duration = (datetime.utcnow() - self.start_time).total_seconds()
            logger.info(f"GOD-MODE COMPLETE: {self.domain} processed in {duration:.2f}s.")
            return {"status": "SUCCESS", "critical_count": len(self.critical_findings)}
            
        except Exception as e:
            logger.error(f"GOD-MODE PIPELINE FAILURE for {self.domain}: {str(e)}")
            return {"status": "FAILED", "error": str(e)}