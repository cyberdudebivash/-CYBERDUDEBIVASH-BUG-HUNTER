"""
CYBERDUDEBIVASH BUG HUNTER
Port Scanner Engine

High-performance asynchronous port scanner for discovered assets.

Features
--------
• Async TCP scanning
• Banner grabbing
• Service detection
• Configurable port lists
• High concurrency support
"""

import asyncio
import socket
from typing import List, Dict


# --------------------------------------------------
# Common service fingerprints
# --------------------------------------------------

COMMON_PORTS = {
    21: "FTP",
    22: "SSH",
    25: "SMTP",
    53: "DNS",
    80: "HTTP",
    110: "POP3",
    143: "IMAP",
    443: "HTTPS",
    3306: "MySQL",
    3389: "RDP",
    5432: "PostgreSQL",
    6379: "Redis",
    8080: "HTTP-Alt",
    8443: "HTTPS-Alt",
}


# --------------------------------------------------
# Port Scanner Engine
# --------------------------------------------------

class PortScanner:

    def __init__(
        self,
        ports: List[int] = None,
        concurrency: int = 500,
        timeout: float = 3.0
    ):

        self.ports = ports if ports else list(COMMON_PORTS.keys())
        self.timeout = timeout
        self.sem = asyncio.Semaphore(concurrency)

    # --------------------------------------------------
    # Scan a single port
    # --------------------------------------------------

    async def scan_port(self, host: str, port: int) -> Dict:

        async with self.sem:

            try:

                reader, writer = await asyncio.wait_for(
                    asyncio.open_connection(host, port),
                    timeout=self.timeout
                )

                banner = ""

                try:

                    writer.write(b"\n")
                    await writer.drain()

                    data = await asyncio.wait_for(
                        reader.read(1024),
                        timeout=1
                    )

                    banner = data.decode(errors="ignore").strip()

                except Exception:
                    pass

                writer.close()

                service = COMMON_PORTS.get(port, "unknown")

                result = {
                    "host": host,
                    "port": port,
                    "service": service,
                    "banner": banner,
                    "status": "open"
                }

                print(f"[PORT] {host}:{port} → OPEN ({service})")

                return result

            except Exception:
                return None

    # --------------------------------------------------
    # Scan host
    # --------------------------------------------------

    async def scan_host(self, host: str) -> List[Dict]:

        tasks = []

        for port in self.ports:

            tasks.append(
                self.scan_port(host, port)
            )

        results = await asyncio.gather(*tasks)

        return [r for r in results if r]

    # --------------------------------------------------
    # Run scanner
    # --------------------------------------------------

    async def run(self, hosts: List[str]) -> List[Dict]:

        results = []

        tasks = []

        for host in hosts:

            tasks.append(
                self.scan_host(host)
            )

        responses = await asyncio.gather(*tasks)

        for r in responses:
            results.extend(r)

        return results


# --------------------------------------------------
# Helper wrapper
# --------------------------------------------------

async def scan_ports(hosts: List[str], ports=None, concurrency=500):

    scanner = PortScanner(
        ports=ports,
        concurrency=concurrency
    )

    return await scanner.run(hosts)


# --------------------------------------------------
# Standalone CLI mode
# --------------------------------------------------

if __name__ == "__main__":

    import sys

    if len(sys.argv) < 2:
        print("Usage: python port_scanner.py host1 host2")
        sys.exit(0)

    targets = sys.argv[1:]

    results = asyncio.run(scan_ports(targets))

    print("\nOpen Ports:\n")

    for r in results:
        print(r)