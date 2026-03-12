"""
CYBERDUDEBIVASH BUG HUNTER
Agentic BOLA (Broken Object Level Authorization) Detection Engine
Focus: High-Impact / Critical Findings for API Security
"""

import asyncio
import aiohttp
import re
import json
from typing import List, Dict, Optional

class BOLAAgent:
    def __init__(self, concurrency: int = 20):
        # High-risk patterns for API endpoints containing IDs
        self.id_patterns = [
            r'/api/v[0-9]/[a-z]+/([0-9a-fA-F-]+)', # UUID/Hash patterns
            r'/api/v[0-9]/[a-z]+/(\d+)',            # Numeric ID patterns
            r'/(?:user|account|order|invoice|profile)/(\d+)'
        ]
        self.semaphore = asyncio.Semaphore(concurrency)

    async def analyze_endpoint(self, session: aiohttp.ClientSession, url: str, headers: Dict):
        """
        Logic: If an ID is found in the URL, attempt to access it 
        with a different/no authorization context.
        """
        for pattern in self.id_patterns:
            match = re.search(pattern, url)
            if match:
                original_id = match.group(1)
                # Logic: Increment/Decrement or mutate the ID to test authorization boundaries
                if original_id.isdigit():
                    test_id = str(int(original_id) + 1)
                else:
                    # For UUIDs, this would typically require a secondary known ID
                    continue 

                test_url = url.replace(original_id, test_id)
                
                async with self.semaphore:
                    try:
                        # Attempt access with potentially lower-privileged headers
                        async with session.get(test_url, headers=headers, timeout=10, ssl=False) as resp:
                            if resp.status == 200:
                                body = await resp.text()
                                # Crucial: Verify if the returned data belongs to a different object
                                if self._is_data_leaked(body, test_id):
                                    return {
                                        "type": "BOLA",
                                        "url": test_url,
                                        "severity": "CRITICAL",
                                        "impact": "Unauthorized Data Access",
                                        "evidence": f"Accessed ID {test_id} via {url}"
                                    }
                    except Exception:
                        pass
        return None

    def _is_data_leaked(self, response_body: str, target_id: str) -> bool:
        """Internal logic to confirm the response actually contains target object data."""
        try:
            data = json.loads(response_body)
            # Check if the response contains the manipulated ID, indicating a successful 'hit'
            return any(str(v) == target_id for v in data.values()) if isinstance(data, dict) else False
        except:
            return target_id in response_body

    async def run_swarm_bola(self, urls: List[str], auth_headers: Optional[Dict] = None):
        """Orchestrate the BOLA swarm against discovered API endpoints."""
        results = []
        headers = auth_headers or {}
        async with aiohttp.ClientSession() as session:
            tasks = [self.analyze_endpoint(session, url, headers) for url in urls]
            findings = await asyncio.gather(*tasks)
            results = [f for f in findings if f]
        
        if results:
            print(f"[CRITICAL] BOLA Agent discovered {len(results)} vulnerabilities!")
        return results