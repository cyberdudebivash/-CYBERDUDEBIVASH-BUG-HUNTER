"""
CYBERDUDEBIVASH BUG HUNTER
Subdomain Permutation Engine

Production-grade permutation engine for discovering additional subdomains
from known assets using mutation strategies and async DNS validation.

Compatible with the CYBERDUDEBIVASH recon pipeline architecture.

Author:
CYBERDUDEBIVASH OFFICIAL AUTHORITY
Founder & CEO, CyberDudeBivash Pvt. Ltd.
"""

import asyncio
import random
from typing import List, Set
import dns.asyncresolver


DEFAULT_WORDLIST = [
    "dev", "test", "stage", "staging", "admin", "beta", "api", "app",
    "internal", "portal", "dashboard", "auth", "cdn", "img", "files",
    "static", "prod", "production", "data", "backup", "old", "new",
    "v1", "v2", "v3"
]


class SubdomainPermutator:
    """
    Generates and validates subdomain permutations.
    """

    def __init__(
        self,
        wordlist: List[str] = None,
        concurrency: int = 200,
        timeout: float = 3.0,
    ):
        self.wordlist = wordlist or DEFAULT_WORDLIST
        self.semaphore = asyncio.Semaphore(concurrency)
        self.timeout = timeout
        self.resolver = dns.asyncresolver.Resolver()

        self.resolver.lifetime = timeout
        self.resolver.timeout = timeout

    # ---------------------------------------------------------
    # Permutation Strategies
    # ---------------------------------------------------------

    def prefix_mutations(self, base: str) -> Set[str]:
        results = set()

        for word in self.wordlist:
            results.add(f"{word}.{base}")

        return results

    def suffix_mutations(self, base: str) -> Set[str]:
        results = set()

        parts = base.split(".")
        if len(parts) < 2:
            return results

        root = ".".join(parts[1:])

        for word in self.wordlist:
            results.add(f"{parts[0]}-{word}.{root}")
            results.add(f"{parts[0]}{word}.{root}")

        return results

    def environment_mutations(self, base: str) -> Set[str]:
        results = set()

        parts = base.split(".")
        if len(parts) < 2:
            return results

        root = ".".join(parts[1:])

        envs = ["dev", "stage", "test", "prod", "uat", "qa"]

        for env in envs:
            results.add(f"{env}-{parts[0]}.{root}")
            results.add(f"{parts[0]}-{env}.{root}")

        return results

    def numeric_mutations(self, base: str) -> Set[str]:
        results = set()

        parts = base.split(".")
        if len(parts) < 2:
            return results

        root = ".".join(parts[1:])

        for i in range(1, 6):
            results.add(f"{parts[0]}{i}.{root}")

        return results

    # ---------------------------------------------------------
    # DNS Validation
    # ---------------------------------------------------------

    async def resolve(self, subdomain: str) -> bool:
        async with self.semaphore:
            try:
                await self.resolver.resolve(subdomain, "A")
                return True
            except Exception:
                return False

    async def validate_batch(self, candidates: Set[str]) -> List[str]:
        tasks = []

        for sub in candidates:
            tasks.append(self.resolve(sub))

        results = await asyncio.gather(*tasks)

        valid = []

        for sub, ok in zip(candidates, results):
            if ok:
                valid.append(sub)

        return valid

    # ---------------------------------------------------------
    # Wildcard Detection
    # ---------------------------------------------------------

    async def detect_wildcard(self, domain: str) -> bool:
        random_label = f"wildcard-test-{random.randint(1000,9999)}.{domain}"

        try:
            await self.resolver.resolve(random_label, "A")
            return True
        except Exception:
            return False

    # ---------------------------------------------------------
    # Main Permutation Engine
    # ---------------------------------------------------------

    async def generate_permutations(self, discovered_subdomains: List[str]) -> List[str]:
        """
        Generate permutations from discovered subdomains.
        """

        permutation_pool = set()

        for sub in discovered_subdomains:

            permutation_pool.update(self.prefix_mutations(sub))
            permutation_pool.update(self.suffix_mutations(sub))
            permutation_pool.update(self.environment_mutations(sub))
            permutation_pool.update(self.numeric_mutations(sub))

        print(f"[PermutationEngine] Generated {len(permutation_pool)} candidates")

        validated = await self.validate_batch(permutation_pool)

        print(f"[PermutationEngine] Valid subdomains discovered: {len(validated)}")

        return validated


# ---------------------------------------------------------
# Standalone Runner (for testing)
# ---------------------------------------------------------

async def run_test():
    engine = SubdomainPermutator()

    discovered = [
        "api.example.com",
        "dev.example.com",
        "app.example.com"
    ]

    results = await engine.generate_permutations(discovered)

    for r in results:
        print("[VALID]", r)


if __name__ == "__main__":
    asyncio.run(run_test())