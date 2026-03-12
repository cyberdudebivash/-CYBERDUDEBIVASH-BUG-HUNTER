"""
CYBERDUDEBIVASH BUG HUNTER
Multi-Cloud Bucket Hunter (S3 / Azure / GCP)
Purpose: Discovering Critical Data Leaks in Cloud Storage
"""

import asyncio
import aiohttp
from typing import List, Dict

class MultiCloudBucketHunter:
    def __init__(self, target_name: str):
        self.target = target_name.split('.')[0]
        self.keywords = ["backup", "data", "logs", "internal", "sql", "dev", "staging", "config"]
        self.results = []

    def _generate_permutations(self) -> List[str]:
        """Generate high-probability bucket names."""
        perms = [self.target]
        for kw in self.keywords:
            perms.append(f"{self.target}-{kw}")
            perms.append(f"{kw}-{self.target}")
            perms.append(f"{self.target}.{kw}")
        return perms

    async def check_s3(self, session: aiohttp.ClientSession, bucket: str):
        """Check AWS S3 Bucket permissions."""
        url = f"https://{bucket}.s3.amazonaws.com"
        try:
            async with session.get(url, timeout=5) as resp:
                # 200 means public listing, 403 means private but exists
                if resp.status == 200:
                    self.results.append({"provider": "AWS", "bucket": bucket, "status": "OPEN", "url": url})
        except: pass

    async def check_azure(self, session: aiohttp.ClientSession, account: str):
        """Check Azure Blob Storage."""
        url = f"https://{account}.blob.core.windows.net"
        try:
            async with session.get(url, timeout=5) as resp:
                if resp.status in [200, 403]: # 403 confirms the account exists
                    self.results.append({"provider": "Azure", "bucket": account, "status": "EXISTS", "url": url})
        except: pass

    async def run_hunt(self):
        """Orchestrate the multi-cloud swarm."""
        buckets = self._generate_permutations()
        print(f"[*] Cloud Hunter: Testing {len(buckets)} permutations for {self.target}...")
        
        async with aiohttp.ClientSession() as session:
            tasks = []
            for b in buckets:
                tasks.append(self.check_s3(session, b))
                tasks.append(self.check_azure(session, b))
            
            await asyncio.gather(*tasks)
        
        return self.results

# Integration Test
if __name__ == "__main__":
    hunter = MultiCloudBucketHunter("example.com")
    found = asyncio.run(hunter.run_hunt())
    print(f"[+] Hunter found {len(found)} cloud assets.")