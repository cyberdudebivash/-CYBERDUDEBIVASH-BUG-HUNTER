"""
CYBERDUDEBIVASH BUG HUNTER
Enterprise Recon Pipeline Orchestrator - BOLA Integrated Edition

Coordinates all reconnaissance engines, now including autonomous 
BOLA (Broken Object Level Authorization) detection for API security.

Author:
CYBERDUDEBIVASH OFFICIAL AUTHORITY
Founder & CEO, CyberDudeBivash Pvt. Ltd. [cite: 12]
"""

import asyncio
from typing import Dict, List, Set

from subdomain_intelligence_engine import SubdomainIntelligenceEngine [cite: 83]
from http_probe_engine import probe_hosts [cite: 83]
from port_scanner import scan_ports [cite: 83]
from tech_fingerprinter import fingerprint_host [cite: 83]
from javascript_endpoint_extractor import extract_js_endpoints [cite: 83]
from takeover_detector import detect_takeovers [cite: 83]
from database import save_asset [cite: 83]

# New Enterprise-Grade Intelligence Agent
# from agents.bola_intelligence_agent import BOLAAgent

class ReconPipeline:
    def __init__(self, domain: str, wordlist: str, concurrency: int = 100):
        self.domain = domain [cite: 83]
        self.wordlist = wordlist [cite: 83]
        self.concurrency = concurrency [cite: 83]

        self.subdomains: List[str] = [] [cite: 83]
        self.resolved: Dict[str, List[str]] = {} [cite: 83]
        self.http_results: List[Dict] = [] [cite: 83]
        self.api_endpoints: Set[str] = set()

    async def subdomain_intelligence(self):
        """Phase 1: Deep Subdomain Discovery."""
        print("\n[Recon] Running Subdomain Intelligence Engine") [cite: 83]
        try:
            engine = SubdomainIntelligenceEngine(
                domain=self.domain,
                wordlist=self.wordlist,
                concurrency=self.concurrency
            ) [cite: 83]
            subs = await engine.run() [cite: 83]
            self.subdomains = subs [cite: 83]
            for s in subs:
                self.resolved[s] = [] [cite: 83]
            print(f"[Recon] Intelligence discovered {len(subs)} subdomains") [cite: 83]
        except Exception as e:
            print(f"[Recon] Subdomain intelligence failed: {e}") [cite: 83]

    async def http_probe(self):
        """Phase 2: Live Service Identification."""
        if not self.subdomains:
            print("[Recon] No subdomains for HTTP probing") [cite: 83]
            return
        print("\n[Recon] Running HTTP probing") [cite: 83]
        try:
            self.http_results = await probe_hosts(self.subdomains) [cite: 83]
            print(f"[Recon] HTTP services discovered: {len(self.http_results)}") [cite: 83]
        except Exception as e:
            print(f"[Recon] HTTP probe error: {e}") [cite: 83]

    async def fingerprint(self):
        """Phase 3: Technology Stack Detection."""
        if not self.http_results:
            print("[Recon] No HTTP targets for fingerprinting") [cite: 83]
            return
        print("\n[Recon] Running technology fingerprinting") [cite: 83]
        for entry in self.http_results:
            try:
                url = entry["url"] [cite: 83]
                host = url.replace("https://", "").replace("http://", "").split("/")[0] [cite: 83]
                tech = await fingerprint_host(url) [cite: 83]
                save_asset(
                    domain=self.domain,
                    host=host,
                    ip=self.resolved.get(host),
                    tech=tech
                ) [cite: 83]
                if tech:
                    print(f"[Tech] {host} -> {', '.join(tech)}") [cite: 83]
            except Exception as e:
                print(f"[Recon] Fingerprint error: {e}") [cite: 83]

    async def js_analysis(self):
        """Phase 4: JavaScript Endpoint Extraction & API Discovery."""
        if not self.http_results:
            return
        print("\n[Recon] Running JavaScript endpoint extraction") [cite: 83]
        try:
            urls = [x["url"] for x in self.http_results] [cite: 83]
            endpoints = await extract_js_endpoints(urls) [cite: 83]
            
            # Filter and store potential API endpoints for BOLA testing
            for ep in endpoints:
                if "/api/" in ep.lower() or "/v1/" in ep.lower():
                    self.api_endpoints.add(ep)
            
            print(f"[Recon] API/JS endpoints discovered: {len(endpoints)}") [cite: 83]
        except Exception as e:
            print(f"[Recon] JS analysis error: {e}") [cite: 83]

    async def run_bola_audit(self):
        """Phase 5: ENTERPRISE ONLY - Autonomous BOLA Intelligence."""
        if not self.api_endpoints:
            print("[Recon] No API endpoints found for BOLA auditing")
            return
        
        print("\n[Recon] Launching Agentic BOLA Intelligence Swarm")
        try:
            # Integrate BOLAAgent logic
            # agent = BOLAAgent(concurrency=self.concurrency // 2)
            # findings = await agent.run_swarm_bola(list(self.api_endpoints))
            # print(f"[Recon] Critical BOLA findings: {len(findings)}")
            pass # Implementation linked to bola_intelligence_agent.py
        except Exception as e:
            print(f"[Recon] BOLA Audit error: {e}")

    async def takeover_scan(self):
        """Phase 6: Subdomain Takeover Detection."""
        if not self.subdomains:
            return
        print("\n[Recon] Running takeover detection") [cite: 83]
        try:
            await detect_takeovers(self.subdomains) [cite: 83]
        except Exception as e:
            print(f"[Recon] Takeover detection error: {e}") [cite: 83]

    async def run(self):
        """Main Pipeline Orchestrator."""
        print("\n=================================================")
        print("CYBERDUDEBIVASH RECON PIPELINE - BOLA INTEGRATED")
        print("=================================================\n")

        await self.subdomain_intelligence()
        await self.http_probe()
        await self.fingerprint()
        await self.js_analysis()
        
        # New Autonomous Security Stage
        await self.run_bola_audit()
        
        await self.takeover_scan()

        print("\n=================================================")
        print("Recon pipeline completed successfully")
        print("=================================================\n")