"""
CYBERDUDEBIVASH BUG HUNTER
HTTP Probe Engine

High-speed HTTP probing engine for discovered hosts.
Designed to integrate with the CYBERDUDEBIVASH Recon Pipeline.

Features:
- Async probing
- HTTP + HTTPS detection
- Title extraction
- Header analysis
- Redirect detection
- Response timing
"""

import asyncio
import time
import re
from typing import List, Dict

import aiohttp


class HTTPProbeEngine:

    def __init__(self, concurrency: int = 100, timeout: int = 10):

        self.concurrency = concurrency
        self.timeout = timeout
        self.sem = asyncio.Semaphore(concurrency)

    async def probe_host(self, session: aiohttp.ClientSession, host: str) -> Dict:

        results = []

        urls = [
            f"http://{host}",
            f"https://{host}"
        ]

        for url in urls:

            async with self.sem:

                try:

                    start = time.time()

                    async with session.get(
                        url,
                        allow_redirects=True,
                        timeout=self.timeout,
                        ssl=False
                    ) as resp:

                        elapsed = round(time.time() - start, 3)

                        body = await resp.text(errors="ignore")

                        title = self.extract_title(body)

                        headers = dict(resp.headers)

                        result = {
                            "url": url,
                            "status": resp.status,
                            "title": title,
                            "server": headers.get("Server"),
                            "length": headers.get("Content-Length"),
                            "redirect": headers.get("Location"),
                            "response_time": elapsed
                        }

                        results.append(result)

                        print(
                            f"[HTTP] {url} "
                            f"[{resp.status}] "
                            f"{title}"
                        )

                except asyncio.TimeoutError:
                    pass

                except aiohttp.ClientError:
                    pass

                except Exception:
                    pass

        return results

    def extract_title(self, html: str) -> str:

        try:

            match = re.search(
                r"<title>(.*?)</title>",
                html,
                re.IGNORECASE | re.DOTALL
            )

            if match:
                return match.group(1).strip()

        except Exception:
            pass

        return ""

    async def run(self, hosts: List[str]) -> List[Dict]:

        results = []

        connector = aiohttp.TCPConnector(limit=0)

        timeout = aiohttp.ClientTimeout(total=self.timeout)

        async with aiohttp.ClientSession(
            connector=connector,
            timeout=timeout
        ) as session:

            tasks = []

            for host in hosts:

                tasks.append(
                    self.probe_host(session, host)
                )

            responses = await asyncio.gather(*tasks)

            for r in responses:
                results.extend(r)

        return results


async def probe_hosts(hosts: List[str], concurrency: int = 100):

    engine = HTTPProbeEngine(concurrency=concurrency)

    return await engine.run(hosts)


# standalone test mode
if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Usage: python http_probe_engine.py host1 host2")
        sys.exit(0)

    hosts = sys.argv[1:]

    results = asyncio.run(probe_hosts(hosts))

    print("\nResults:")

    for r in results:
        print(r)