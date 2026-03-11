import asyncio
from typing import Dict, List

from subdomain_intelligence_engine import SubdomainIntelligenceEngine
from http_probe_engine import probe_hosts
from port_scanner import scan_ports
from tech_fingerprinter import fingerprint_host
from javascript_endpoint_extractor import extract_js_endpoints
from takeover_detector import detect_takeovers
from database import save_asset


class ReconPipeline:

    def __init__(self, domain: str, wordlist: str, concurrency: int = 100):

        self.domain = domain
        self.wordlist = wordlist
        self.concurrency = concurrency

        self.subdomains: List[str] = []
        self.resolved: Dict[str, List[str]] = {}
        self.http_results: List[Dict] = []

    # ----------------------------------------------------------------
    # SUBDOMAIN INTELLIGENCE
    # ----------------------------------------------------------------

    async def subdomain_intelligence(self):

        print("\n[Recon] Running Subdomain Intelligence Engine")

        try:

            engine = SubdomainIntelligenceEngine(
                domain=self.domain,
                wordlist=self.wordlist,
                concurrency=self.concurrency
            )

            subs = await engine.run()

            self.subdomains = subs

            for s in subs:
                self.resolved[s] = []

            print(f"[Recon] Intelligence discovered {len(subs)} subdomains")

        except Exception as e:

            print(f"[Recon] Subdomain intelligence failed: {e}")

    # ----------------------------------------------------------------
    # HTTP PROBING
    # ----------------------------------------------------------------

    async def http_probe(self):

        if not self.subdomains:
            print("[Recon] No subdomains for HTTP probing")
            return

        print("\n[Recon] Running HTTP probing")

        try:

            self.http_results = await probe_hosts(self.subdomains)

            print(f"[Recon] HTTP services discovered: {len(self.http_results)}")

        except Exception as e:

            print(f"[Recon] HTTP probe error: {e}")

    # ----------------------------------------------------------------
    # PORT SCANNING
    # ----------------------------------------------------------------

    async def port_scan(self):

        if not self.subdomains:
            return

        print("\n[Recon] Running port scanning")

        try:

            await scan_ports(self.subdomains)

        except Exception as e:

            print(f"[Recon] Port scan error: {e}")

    # ----------------------------------------------------------------
    # TECHNOLOGY FINGERPRINTING
    # ----------------------------------------------------------------

    async def fingerprint(self):

        if not self.http_results:
            print("[Recon] No HTTP targets for fingerprinting")
            return

        print("\n[Recon] Running technology fingerprinting")

        for entry in self.http_results:

            try:

                url = entry["url"]

                host = (
                    url.replace("https://", "")
                    .replace("http://", "")
                    .split("/")[0]
                )

                tech = await fingerprint_host(url)

                save_asset(
                    domain=self.domain,
                    host=host,
                    ip=self.resolved.get(host),
                    tech=tech
                )

                if tech:
                    print(f"[Tech] {host} -> {', '.join(tech)}")

            except Exception as e:

                print(f"[Recon] Fingerprint error: {e}")

    # ----------------------------------------------------------------
    # JAVASCRIPT ANALYSIS
    # ----------------------------------------------------------------

    async def js_analysis(self):

        if not self.http_results:
            return

        print("\n[Recon] Running JavaScript endpoint extraction")

        try:

            urls = [x["url"] for x in self.http_results]

            endpoints = await extract_js_endpoints(urls)

            print(f"[Recon] JS endpoints discovered: {len(endpoints)}")

        except Exception as e:

            print(f"[Recon] JS analysis error: {e}")

    # ----------------------------------------------------------------
    # SUBDOMAIN TAKEOVER DETECTION
    # ----------------------------------------------------------------

    async def takeover_scan(self):

        if not self.subdomains:
            return

        print("\n[Recon] Running takeover detection")

        try:

            await detect_takeovers(self.subdomains)

        except Exception as e:

            print(f"[Recon] Takeover detection error: {e}")

    # ----------------------------------------------------------------
    # PIPELINE ORCHESTRATOR
    # ----------------------------------------------------------------

    async def run(self):

        print("\n=================================================")
        print("CYBERDUDEBIVASH RECON PIPELINE")
        print("=================================================\n")

        await self.subdomain_intelligence()

        await self.http_probe()

        await self.port_scan()

        await self.fingerprint()

        await self.js_analysis()

        await self.takeover_scan()

        print("\n=================================================")
        print("Recon pipeline completed")
        print("=================================================\n")