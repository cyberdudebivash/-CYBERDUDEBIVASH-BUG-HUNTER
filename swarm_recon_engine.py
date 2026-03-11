import asyncio
import socket
import aiodns
import argparse
from pathlib import Path


class SwarmReconEngine:
    """
    CYBERDUDEBIVASH Swarm Recon Engine

    Async subdomain DNS reconnaissance engine
    """

    def __init__(self, domain: str, wordlist: str, concurrency: int = 100):

        self.domain = domain.strip()
        self.wordlist = Path(wordlist)
        self.concurrency = concurrency

        if not self.wordlist.exists():
            raise FileNotFoundError(f"Wordlist not found: {wordlist}")

        self.resolver = None
        self.sem = asyncio.Semaphore(self.concurrency)
        self.results = []

    async def initialize(self):
        """Initialize async DNS resolver inside the running loop"""
        self.resolver = aiodns.DNSResolver()

    async def resolve_subdomain(self, subdomain: str):

        target = f"{subdomain}.{self.domain}"

        async with self.sem:

            try:
                response = await self.resolver.getaddrinfo(
                    target,
                    0,
                    socket.AF_INET,
                    socket.SOCK_STREAM
                )

                ips = list({r[4][0] for r in response})

                result = {
                    "host": target,
                    "ips": ips
                }

                self.results.append(result)

                print(f"[+] {target} -> {ips}")

            except aiodns.error.DNSError:
                pass

            except Exception as e:
                print(f"[ERROR] {target} : {e}")

    async def run(self):

        await self.initialize()

        tasks = []

        with open(self.wordlist, "r", encoding="utf-8", errors="ignore") as f:

            for line in f:

                sub = line.strip()

                if not sub:
                    continue

                tasks.append(
                    asyncio.create_task(
                        self.resolve_subdomain(sub)
                    )
                )

        print(f"\n[SwarmRecon] Starting scan against {self.domain}")
        print(f"[SwarmRecon] Wordlist size: {len(tasks)}")
        print(f"[SwarmRecon] Concurrency: {self.concurrency}\n")

        await asyncio.gather(*tasks)

        print("\n[SwarmRecon] Scan completed")
        print(f"[SwarmRecon] Resolved hosts: {len(self.results)}")

        return self.results


def run_swarm(domain: str, wordlist: str, concurrency: int):

    engine = SwarmReconEngine(domain, wordlist, concurrency)

    asyncio.run(engine.run())


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description="CyberDudeBivash Swarm Recon Engine"
    )

    parser.add_argument(
        "-d", "--domain",
        required=True,
        help="Target domain"
    )

    parser.add_argument(
        "-w", "--wordlist",
        required=True,
        help="Subdomain wordlist"
    )

    parser.add_argument(
        "-c", "--concurrency",
        default=100,
        type=int,
        help="Concurrency level"
    )

    args = parser.parse_args()

    run_swarm(
        domain=args.domain,
        wordlist=args.wordlist,
        concurrency=args.concurrency
    )