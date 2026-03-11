import asyncio
import aiodns


class MassDNSResolver:

    def __init__(self):
        self.resolver = aiodns.DNSResolver(
            nameservers=["8.8.8.8", "1.1.1.1"]
        )

    async def resolve(self, domain):

        try:
            result = await self.resolver.query(domain, "A")
            return domain, [r.host for r in result]

        except:
            return None

    async def run(self, domains):

        tasks = [self.resolve(d) for d in domains]

        results = await asyncio.gather(*tasks)

        return [r for r in results if r]