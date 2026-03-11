import asyncio
from intel.chaos_client import fetch_chaos
from intel.alienvault_client import fetch_otx
from intel.crt_client import fetch_crt


class PassiveReconAggregator:

    def __init__(self, domain):
        self.domain = domain

    async def run(self):

        results = await asyncio.gather(
            fetch_crt(self.domain),
            fetch_chaos(self.domain),
            fetch_otx(self.domain)
        )

        subs = set()

        for r in results:
            subs.update(r)

        return list(subs)