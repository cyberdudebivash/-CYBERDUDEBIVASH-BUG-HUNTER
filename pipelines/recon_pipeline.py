"""
CYBERDUDEBIVASH BUG HUNTER
Enterprise Recon Pipeline Orchestrator

Coordinates all reconnaissance engines to perform a full attack surface
mapping workflow.

Author:
CYBERDUDEBIVASH OFFICIAL AUTHORITY
Founder & CEO, CyberDudeBivash Pvt. Ltd.
"""

import asyncio
from typing import Set, Dict

from engines.recon.swarm_recon_engine import SwarmReconEngine
from engines.recon.http_probe_engine import HTTPProbeEngine
from engines.recon.port_scanner import PortScanner
from engines.recon.tech_fingerprinter import TechFingerprinter
from engines.recon.javascript_endpoint_extractor import JavascriptEndpointExtractor
from engines.recon.takeover_detector import TakeoverDetector
from engines.recon.subdomain_intelligence_engine import SubdomainIntelligenceEngine

from engines.discovery.subdomain_permutator import SubdomainPermutator
from engines.discovery.web_crawler import WebCrawler

from database.database import Database


class ReconPipeline:

    def __init__(self, target: str):

        self.target = target

        # -------------------------------
        # Recon Engines
        # -------------------------------

        self.swarm_engine = SwarmReconEngine()
        self.subdomain_intel = SubdomainIntelligenceEngine()
        self.permutator = SubdomainPermutator()

        self.http_probe = HTTPProbeEngine()
        self.port_scanner = PortScanner()
        self.tech_fingerprinter = TechFingerprinter()

        self.crawler = WebCrawler()
        self.js_extractor = JavascriptEndpointExtractor()
        self.takeover_detector = TakeoverDetector()

        # -------------------------------
        # Storage Layer
        # -------------------------------

        self.db = Database()

        # -------------------------------
        # Asset Collections
        # -------------------------------

        self.subdomains: Set[str] = set()
        self.live_hosts: Set[str] = set()

        self.urls: Set[str] = set()
        self.js_files: Set[str] = set()

        self.endpoints: Set[str] = set()
        self.parameters: Set[str] = set()
        self.forms = []

    # -------------------------------------------------------
    # STEP 1 — Subdomain Discovery
    # -------------------------------------------------------

    async def discover_subdomains(self):

        print(f"[PIPELINE] Starting swarm recon for {self.target}")

        discovered = await self.swarm_engine.enumerate(self.target)

        self.subdomains.update(discovered)

        print(f"[PIPELINE] Subdomains discovered: {len(self.subdomains)}")

    # -------------------------------------------------------
    # STEP 2 — Subdomain Intelligence
    # -------------------------------------------------------

    async def enrich_subdomains(self):

        print("[PIPELINE] Running subdomain intelligence")

        enriched = await self.subdomain_intel.enrich(list(self.subdomains))

        self.subdomains.update(enriched)

        print(f"[PIPELINE] Subdomains after enrichment: {len(self.subdomains)}")

    # -------------------------------------------------------
    # STEP 3 — Subdomain Permutation Engine
    # -------------------------------------------------------

    async def run_permutation_engine(self):

        print("[PIPELINE] Running permutation engine")

        before = len(self.subdomains)

        new_subdomains = await self.permutator.generate_permutations(
            list(self.subdomains)
        )

        self.subdomains.update(new_subdomains)

        after = len(self.subdomains)

        print(f"[PIPELINE] Permutation discovered {after - before} new assets")

    # -------------------------------------------------------
    # STEP 4 — HTTP Probing
    # -------------------------------------------------------

    async def probe_live_hosts(self):

        print("[PIPELINE] Probing HTTP services")

        results = await self.http_probe.probe(list(self.subdomains))

        for item in results:

            host = item.get("host")
            url = item.get("url")

            if host:
                self.live_hosts.add(host)

            if url:
                self.urls.add(url)

        print(f"[PIPELINE] Live hosts discovered: {len(self.live_hosts)}")

    # -------------------------------------------------------
    # STEP 5 — Port Scanning
    # -------------------------------------------------------

    async def scan_ports(self):

        print("[PIPELINE] Running port scanner")

        results = await self.port_scanner.scan(list(self.live_hosts))

        for r in results:
            await self.db.save_port_scan(r)

        print("[PIPELINE] Port scanning completed")

    # -------------------------------------------------------
    # STEP 6 — Technology Fingerprinting
    # -------------------------------------------------------

    async def fingerprint_technologies(self):

        print("[PIPELINE] Running tech fingerprinting")

        results = await self.tech_fingerprinter.fingerprint(
            list(self.live_hosts)
        )

        for r in results:
            await self.db.save_technology(r)

        print("[PIPELINE] Technology detection completed")

    # -------------------------------------------------------
    # STEP 7 — Web Crawling
    # -------------------------------------------------------

    async def run_crawler(self):

        print("[PIPELINE] Starting web crawler")

        results = await self.crawler.run(list(self.live_hosts))

        self.urls.update(results["urls"])
        self.js_files.update(results["js_files"])
        self.endpoints.update(results["endpoints"])
        self.parameters.update(results["parameters"])
        self.forms.extend(results["forms"])

        print(f"[PIPELINE] URLs discovered: {len(self.urls)}")
        print(f"[PIPELINE] JS files discovered: {len(self.js_files)}")

    # -------------------------------------------------------
    # STEP 8 — Javascript Endpoint Extraction
    # -------------------------------------------------------

    async def extract_js_endpoints(self):

        print("[PIPELINE] Running JS endpoint extractor")

        endpoints = await self.js_extractor.extract_endpoints(
            list(self.js_files)
        )

        for ep in endpoints:
            self.endpoints.add(ep)

        print(f"[PIPELINE] Total endpoints discovered: {len(self.endpoints)}")

    # -------------------------------------------------------
    # STEP 9 — Subdomain Takeover Detection
    # -------------------------------------------------------

    async def detect_takeovers(self):

        print("[PIPELINE] Running takeover detector")

        findings = await self.takeover_detector.detect(
            list(self.subdomains)
        )

        for finding in findings:
            await self.db.save_takeover(finding)

        print("[PIPELINE] Takeover detection completed")

    # -------------------------------------------------------
    # STEP 10 — Persist All Assets
    # -------------------------------------------------------

    async def persist_assets(self):

        print("[PIPELINE] Persisting discovered assets")

        for sub in self.subdomains:
            await self.db.save_subdomain(sub)

        for host in self.live_hosts:
            await self.db.save_host(host)

        for url in self.urls:
            await self.db.save_url(url)

        for js in self.js_files:
            await self.db.save_javascript(js)

        for ep in self.endpoints:
            await self.db.save_endpoint(ep)

        print("[PIPELINE] Asset persistence complete")

    # -------------------------------------------------------
    # MAIN PIPELINE EXECUTION
    # -------------------------------------------------------

    async def run(self) -> Dict:

        print("\n===================================")
        print(" CYBERDUDEBIVASH BUG HUNTER ")
        print(" ENTERPRISE RECON PIPELINE ")
        print("===================================\n")

        await self.discover_subdomains()

        await self.enrich_subdomains()

        await self.run_permutation_engine()

        await self.probe_live_hosts()

        await self.scan_ports()

        await self.fingerprint_technologies()

        await self.run_crawler()

        await self.extract_js_endpoints()

        await self.detect_takeovers()

        await self.persist_assets()

        print("\n[PIPELINE] Recon Completed Successfully\n")

        return {
            "subdomains": list(self.subdomains),
            "live_hosts": list(self.live_hosts),
            "urls": list(self.urls),
            "javascript_files": list(self.js_files),
            "endpoints": list(self.endpoints),
            "parameters": list(self.parameters),
            "forms": self.forms
        }


# -------------------------------------------------------
# Standalone Runner
# -------------------------------------------------------

async def run_pipeline(target: str):

    pipeline = ReconPipeline(target)

    results = await pipeline.run()

    print("\n========== RECON SUMMARY ==========")
    print("Subdomains:", len(results["subdomains"]))
    print("Live Hosts:", len(results["live_hosts"]))
    print("URLs:", len(results["urls"]))
    print("Javascript Files:", len(results["javascript_files"]))
    print("Endpoints:", len(results["endpoints"]))
    print("Parameters:", len(results["parameters"]))
    print("Forms:", len(results["forms"]))
    print("===================================")


if __name__ == "__main__":

    target = "example.com"

    asyncio.run(run_pipeline(target))