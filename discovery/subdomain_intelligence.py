import asyncio
from discovery.ct_logs import fetch_ct_subdomains
from discovery.dns_bruteforce import dns_bruteforce


class SubdomainIntelligence:

    def __init__(self, domain, wordlist):
        self.domain = domain
        self.wordlist = wordlist

    async def run(self):

        passive = await fetch_ct_subdomains(self.domain)

        active = await dns_bruteforce(self.domain, self.wordlist)

        results = set(passive + active)

        print(f"[INTEL] discovered {len(results)} unique subdomains")

        return list(results)