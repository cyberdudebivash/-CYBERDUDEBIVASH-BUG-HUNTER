import aiohttp
import asyncio


class PassiveReconEngine:
    def __init__(self, domain):
        self.domain = domain

    async def chaos(self):
        url = f"https://dns.projectdiscovery.io/dns/{self.domain}/subdomains"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.json()
                    return [f"{sub}.{self.domain}" for sub in data.get("subdomains", [])]
        except Exception:
            return []

    async def alienvault(self):
        url = f"https://otx.alienvault.com/api/v1/indicators/domain/{self.domain}/passive_dns"

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as r:
                    data = await r.json()
                    return [entry["hostname"] for entry in data.get("passive_dns", [])]
        except Exception:
            return []

    async def run(self):
        results = await asyncio.gather(
            self.chaos(),
            self.alienvault()
        )

        subs = set()
        for r in results:
            subs.update(r)

        return list(subs)