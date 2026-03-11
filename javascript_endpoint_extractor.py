"""
CYBERDUDEBIVASH BUG HUNTER
JavaScript Endpoint Extraction Engine

Capabilities
------------
• Discover JavaScript files from webpages
• Download JS files asynchronously
• Extract API endpoints, URLs, paths
• Detect tokens / keys
• Return structured intelligence

Designed for integration with recon_pipeline.py
"""

import asyncio
import re
from typing import List, Dict
from urllib.parse import urljoin, urlparse

import aiohttp


# ----------------------------------------------------------
# Regex patterns
# ----------------------------------------------------------

ENDPOINT_REGEX = re.compile(
    r"""(?:"|')(
        (?:https?:\/\/[^\s"']+) |
        (?:\/[a-zA-Z0-9_\-\/\.]+)
    )(?:"|')""",
    re.VERBOSE
)

API_REGEX = re.compile(
    r"""(?:"|')(
        (?:\/api\/[a-zA-Z0-9_\-\/\.]+)
    )(?:"|')""",
    re.VERBOSE
)

TOKEN_REGEX = re.compile(
    r"""(?:"|')(
        (?:AKIA[0-9A-Z]{16}) |
        (?:AIza[0-9A-Za-z\-_]{35}) |
        (?:sk_live_[0-9a-zA-Z]{24})
    )(?:"|')""",
    re.VERBOSE
)

JS_FILE_REGEX = re.compile(
    r'<script[^>]+src=["\'](.*?)["\']',
    re.IGNORECASE
)


# ----------------------------------------------------------
# JavaScript extractor engine
# ----------------------------------------------------------

class JavaScriptEndpointExtractor:

    def __init__(self, concurrency: int = 50, timeout: int = 10):

        self.sem = asyncio.Semaphore(concurrency)
        self.timeout = timeout

    # ------------------------------------------------------
    # Fetch URL
    # ------------------------------------------------------

    async def fetch(self, session, url):

        try:

            async with self.sem:

                async with session.get(
                    url,
                    timeout=self.timeout,
                    ssl=False
                ) as resp:

                    return await resp.text(errors="ignore")

        except Exception:
            return ""

    # ------------------------------------------------------
    # Discover JS files
    # ------------------------------------------------------

    def discover_js_files(self, html: str, base_url: str):

        js_files = set()

        matches = JS_FILE_REGEX.findall(html)

        for match in matches:

            js_url = urljoin(base_url, match)

            js_files.add(js_url)

        return list(js_files)

    # ------------------------------------------------------
    # Extract endpoints
    # ------------------------------------------------------

    def extract_endpoints(self, js_content: str):

        endpoints = set()

        for match in ENDPOINT_REGEX.findall(js_content):
            endpoints.add(match)

        for match in API_REGEX.findall(js_content):
            endpoints.add(match)

        return list(endpoints)

    # ------------------------------------------------------
    # Extract secrets
    # ------------------------------------------------------

    def extract_tokens(self, js_content: str):

        tokens = set()

        for match in TOKEN_REGEX.findall(js_content):
            tokens.add(match)

        return list(tokens)

    # ------------------------------------------------------
    # Process single host
    # ------------------------------------------------------

    async def analyze_host(self, session, url: str):

        results = {
            "host": url,
            "javascript_files": [],
            "endpoints": [],
            "tokens": []
        }

        html = await self.fetch(session, url)

        if not html:
            return results

        js_files = self.discover_js_files(html, url)

        results["javascript_files"] = js_files

        tasks = []

        for js_url in js_files:

            tasks.append(
                self.fetch(session, js_url)
            )

        responses = await asyncio.gather(*tasks)

        for js_content in responses:

            endpoints = self.extract_endpoints(js_content)

            tokens = self.extract_tokens(js_content)

            results["endpoints"].extend(endpoints)

            results["tokens"].extend(tokens)

        results["endpoints"] = list(set(results["endpoints"]))
        results["tokens"] = list(set(results["tokens"]))

        if results["endpoints"]:

            print(
                f"[JS] {url} → {len(results['endpoints'])} endpoints"
            )

        if results["tokens"]:

            print(
                f"[JS] {url} → {len(results['tokens'])} potential secrets"
            )

        return results

    # ------------------------------------------------------
    # Run extractor
    # ------------------------------------------------------

    async def run(self, urls: List[str]) -> List[Dict]:

        results = []

        timeout = aiohttp.ClientTimeout(total=self.timeout)

        async with aiohttp.ClientSession(timeout=timeout) as session:

            tasks = []

            for url in urls:

                tasks.append(
                    self.analyze_host(session, url)
                )

            responses = await asyncio.gather(*tasks)

            results.extend(responses)

        return results


# ----------------------------------------------------------
# Helper wrapper
# ----------------------------------------------------------

async def extract_js_endpoints(urls: List[str]):

    engine = JavaScriptEndpointExtractor()

    return await engine.run(urls)


# ----------------------------------------------------------
# Standalone test
# ----------------------------------------------------------

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:

        print("Usage: python javascript_endpoint_extractor.py https://target.com")

        sys.exit(0)

    targets = sys.argv[1:]

    results = asyncio.run(extract_js_endpoints(targets))

    print("\nResults:\n")

    for r in results:

        print(r)