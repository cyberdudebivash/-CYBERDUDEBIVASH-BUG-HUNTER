"""
CYBERDUDEBIVASH BUG HUNTER
Subdomain Takeover Detection Engine

Detects potential subdomain takeover vulnerabilities by analyzing:
- DNS CNAME records
- HTTP response fingerprints
- Provider-specific error messages

Designed for integration with the CYBERDUDEBIVASH recon pipeline.
"""

import asyncio
import socket
from typing import List, Dict

import aiohttp
import aiodns


# ------------------------------------------------------------
# Known takeover fingerprints
# ------------------------------------------------------------

TAKEOVER_FINGERPRINTS = {
    "AWS S3": [
        "NoSuchBucket",
        "The specified bucket does not exist"
    ],
    "GitHub Pages": [
        "There isn't a GitHub Pages site here"
    ],
    "Heroku": [
        "No such app"
    ],
    "Azure": [
        "The resource you are looking for has been removed"
    ],
    "Fastly": [
        "Fastly error: unknown domain"
    ],
    "CloudFront": [
        "The request could not be satisfied"
    ]
}


# ------------------------------------------------------------
# DNS CNAME lookup
# ------------------------------------------------------------

class DNSResolver:

    def __init__(self):
        self.resolver = aiodns.DNSResolver()

    async def get_cname(self, host: str):

        try:
            result = await self.resolver.query(host, "CNAME")

            if result:
                return result[0].host

        except Exception:
            pass

        return None


# ------------------------------------------------------------
# HTTP fingerprint scanner
# ------------------------------------------------------------

class HTTPFingerprintScanner:

    def __init__(self, timeout=8):

        self.timeout = timeout

    async def fetch(self, session, url):

        try:

            async with session.get(
                url,
                timeout=self.timeout,
                ssl=False,
                allow_redirects=True
            ) as resp:

                body = await resp.text(errors="ignore")

                return resp.status, body

        except Exception:
            return None, ""


# ------------------------------------------------------------
# Takeover detection engine
# ------------------------------------------------------------

class TakeoverDetector:

    def __init__(self, concurrency=50):

        self.concurrency = concurrency
        self.sem = asyncio.Semaphore(concurrency)

        self.dns = DNSResolver()
        self.http = HTTPFingerprintScanner()

    async def analyze_host(self, session, host: str):

        findings = []

        cname = await self.dns.get_cname(host)

        if not cname:
            return None

        urls = [
            f"http://{host}",
            f"https://{host}"
        ]

        for url in urls:

            async with self.sem:

                status, body = await self.http.fetch(session, url)

                if not body:
                    continue

                for provider, fingerprints in TAKEOVER_FINGERPRINTS.items():

                    for fp in fingerprints:

                        if fp.lower() in body.lower():

                            finding = {
                                "host": host,
                                "provider": provider,
                                "cname": cname,
                                "url": url,
                                "indicator": fp,
                                "severity": "HIGH",
                                "type": "subdomain_takeover"
                            }

                            findings.append(finding)

                            print(
                                f"[TAKEOVER] {host} → {provider} "
                                f"(indicator: {fp})"
                            )

        if findings:
            return findings

        return None

    async def run(self, hosts: List[str]) -> List[Dict]:

        results = []

        timeout = aiohttp.ClientTimeout(total=10)

        async with aiohttp.ClientSession(timeout=timeout) as session:

            tasks = []

            for host in hosts:

                tasks.append(
                    self.analyze_host(session, host)
                )

            responses = await asyncio.gather(*tasks)

            for r in responses:
                if r:
                    results.extend(r)

        return results


# ------------------------------------------------------------
# Helper wrapper
# ------------------------------------------------------------

async def detect_takeovers(hosts: List[str], concurrency=50):

    engine = TakeoverDetector(concurrency)

    return await engine.run(hosts)


# ------------------------------------------------------------
# Standalone mode
# ------------------------------------------------------------

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Usage: python takeover_detector.py host1 host2")
        sys.exit(0)

    hosts = sys.argv[1:]

    results = asyncio.run(detect_takeovers(hosts))

    print("\nPotential takeover findings:")

    for r in results:
        print(r)