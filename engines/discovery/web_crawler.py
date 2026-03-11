"""
CYBERDUDEBIVASH BUG HUNTER
Advanced Web Crawler Engine

High-performance asynchronous crawler for discovering
endpoints, parameters, forms, and JavaScript assets.

Designed for integration with the CYBERDUDEBIVASH
Enterprise Recon Pipeline.

Author:
CYBERDUDEBIVASH OFFICIAL AUTHORITY
Founder & CEO, CyberDudeBivash Pvt. Ltd.
"""

import asyncio
import re
from urllib.parse import urljoin, urlparse, parse_qs

import aiohttp
from bs4 import BeautifulSoup


DEFAULT_HEADERS = {
    "User-Agent": "CyberDudeBivash-BugHunter/1.0"
}


class WebCrawler:

    def __init__(
        self,
        concurrency: int = 30,
        timeout: int = 10,
        max_depth: int = 2,
    ):

        self.semaphore = asyncio.Semaphore(concurrency)
        self.timeout = timeout
        self.max_depth = max_depth

        self.visited = set()
        self.discovered_urls = set()
        self.js_files = set()
        self.endpoints = set()
        self.parameters = set()
        self.forms = []

    # ------------------------------------------------
    # HTTP FETCH
    # ------------------------------------------------

    async def fetch(self, session: aiohttp.ClientSession, url: str):

        async with self.semaphore:

            try:

                async with session.get(
                    url,
                    timeout=self.timeout,
                    allow_redirects=True,
                    headers=DEFAULT_HEADERS,
                ) as response:

                    if response.status != 200:
                        return None

                    content_type = response.headers.get("content-type", "")

                    if "text/html" not in content_type:
                        return None

                    text = await response.text()

                    return text

            except Exception:
                return None

    # ------------------------------------------------
    # LINK EXTRACTION
    # ------------------------------------------------

    def extract_links(self, html: str, base_url: str):

        soup = BeautifulSoup(html, "html.parser")

        links = set()

        for tag in soup.find_all("a", href=True):

            href = tag["href"]

            absolute = urljoin(base_url, href)

            links.add(absolute)

        return links

    # ------------------------------------------------
    # JS FILE DISCOVERY
    # ------------------------------------------------

    def extract_js_files(self, html: str, base_url: str):

        soup = BeautifulSoup(html, "html.parser")

        for script in soup.find_all("script", src=True):

            src = script["src"]

            js_url = urljoin(base_url, src)

            self.js_files.add(js_url)

    # ------------------------------------------------
    # FORM DISCOVERY
    # ------------------------------------------------

    def extract_forms(self, html: str, base_url: str):

        soup = BeautifulSoup(html, "html.parser")

        for form in soup.find_all("form"):

            action = form.get("action")

            method = form.get("method", "GET")

            action_url = urljoin(base_url, action) if action else base_url

            inputs = []

            for inp in form.find_all("input"):

                name = inp.get("name")

                if name:
                    inputs.append(name)

            self.forms.append({
                "action": action_url,
                "method": method,
                "inputs": inputs
            })

    # ------------------------------------------------
    # PARAMETER EXTRACTION
    # ------------------------------------------------

    def extract_parameters(self, url: str):

        parsed = urlparse(url)

        query = parsed.query

        if not query:
            return

        params = parse_qs(query)

        for p in params:
            self.parameters.add(p)

    # ------------------------------------------------
    # ENDPOINT EXTRACTION
    # ------------------------------------------------

    def extract_api_paths(self, html: str):

        pattern = r"/api/[a-zA-Z0-9_\-/]+"

        matches = re.findall(pattern, html)

        for m in matches:
            self.endpoints.add(m)

    # ------------------------------------------------
    # URL NORMALIZATION
    # ------------------------------------------------

    def normalize_url(self, url: str):

        parsed = urlparse(url)

        return f"{parsed.scheme}://{parsed.netloc}{parsed.path}"

    # ------------------------------------------------
    # DOMAIN FILTER
    # ------------------------------------------------

    def same_domain(self, base: str, target: str):

        base_domain = urlparse(base).netloc
        target_domain = urlparse(target).netloc

        return base_domain == target_domain

    # ------------------------------------------------
    # PAGE PROCESSOR
    # ------------------------------------------------

    async def process_page(self, session, url, base_url, depth):

        if url in self.visited:
            return []

        self.visited.add(url)

        html = await self.fetch(session, url)

        if not html:
            return []

        self.discovered_urls.add(url)

        self.extract_parameters(url)

        self.extract_js_files(html, base_url)

        self.extract_forms(html, base_url)

        self.extract_api_paths(html)

        links = self.extract_links(html, base_url)

        next_links = []

        for link in links:

            if not self.same_domain(base_url, link):
                continue

            normalized = self.normalize_url(link)

            if normalized not in self.visited:
                next_links.append(normalized)

        return next_links

    # ------------------------------------------------
    # BFS CRAWLER
    # ------------------------------------------------

    async def crawl(self, start_urls):

        queue = []

        for url in start_urls:
            queue.append((url, 0))

        async with aiohttp.ClientSession() as session:

            while queue:

                url, depth = queue.pop(0)

                if depth > self.max_depth:
                    continue

                children = await self.process_page(
                    session,
                    url,
                    url,
                    depth
                )

                for child in children:

                    queue.append((child, depth + 1))

        return {
            "urls": list(self.discovered_urls),
            "js_files": list(self.js_files),
            "endpoints": list(self.endpoints),
            "parameters": list(self.parameters),
            "forms": self.forms
        }

    # ------------------------------------------------
    # PIPELINE INTEGRATION
    # ------------------------------------------------

    async def run(self, hosts):

        start_urls = []

        for host in hosts:

            if not host.startswith("http"):
                start_urls.append(f"https://{host}")
                start_urls.append(f"http://{host}")
            else:
                start_urls.append(host)

        results = await self.crawl(start_urls)

        print(f"[Crawler] URLs discovered: {len(results['urls'])}")
        print(f"[Crawler] JS files discovered: {len(results['js_files'])}")
        print(f"[Crawler] API endpoints discovered: {len(results['endpoints'])}")
        print(f"[Crawler] Parameters discovered: {len(results['parameters'])}")
        print(f"[Crawler] Forms discovered: {len(results['forms'])}")

        return results


# ------------------------------------------------
# STANDALONE TEST MODE
# ------------------------------------------------

async def run_test():

    crawler = WebCrawler(
        concurrency=20,
        max_depth=2
    )

    targets = [
        "https://example.com"
    ]

    results = await crawler.run(targets)

    print("\nSummary")
    print("URLs:", len(results["urls"]))
    print("JS:", len(results["js_files"]))
    print("Endpoints:", len(results["endpoints"]))
    print("Parameters:", len(results["parameters"]))
    print("Forms:", len(results["forms"]))


if __name__ == "__main__":

    asyncio.run(run_test())