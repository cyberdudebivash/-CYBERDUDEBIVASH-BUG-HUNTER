import asyncio
import aiohttp
import json
from swarm_recon_engine import SwarmReconEngine

CRT_API = "https://crt.sh/?q=%25.{domain}&output=json"


class SubdomainIntelligenceEngine:

    def __init__(self, domain, wordlist, concurrency=100):

        self.domain = domain
        self.wordlist = wordlist
        self.concurrency = concurrency

        self.passive_subdomains = set()
        self.active_subdomains = set()

    async def fetch_ct_logs(self):

        print("[INTEL] Fetching CT logs")

        url = CRT_API.format(domain=self.domain)

        try:

            async with aiohttp.ClientSession() as session:

                async with session.get(url, timeout=30) as resp:

                    if resp.status != 200:
                        return

                    data = await resp.json(content_type=None)

                    for entry in data:

                        name = entry.get("name_value")

                        if not name:
                            continue

                        for sub in name.split("\n"):

                            sub = sub.strip()

                            if self.domain in sub:
                                self.passive_subdomains.add(sub)

        except Exception as e:

            print(f"[INTEL] CT fetch error: {e}")

        print(f"[INTEL] CT discovered {len(self.passive_subdomains)} subdomains")

    async def active_dns_bruteforce(self):

        print("[INTEL] Running active DNS bruteforce")

        engine = SwarmReconEngine(
            domain=self.domain,
            wordlist=self.wordlist,
            concurrency=self.concurrency
        )

        results = await engine.run()

        for r in results:
            self.active_subdomains.add(r["host"])

        print(f"[INTEL] Active discovered {len(self.active_subdomains)} hosts")

    async def run(self):

        await self.fetch_ct_logs()

        await self.active_dns_bruteforce()

        all_subdomains = set()

        all_subdomains.update(self.passive_subdomains)
        all_subdomains.update(self.active_subdomains)

        print(f"[INTEL] Total unique subdomains: {len(all_subdomains)}")

        return list(all_subdomains)