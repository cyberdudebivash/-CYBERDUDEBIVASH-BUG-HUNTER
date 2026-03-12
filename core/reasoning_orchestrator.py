"""
CYBERDUDEBIVASH GOD MODE - AI Reasoning Brain
Path: core/reasoning_orchestrator.py
Purpose: Strategic attack path expansion and autonomous swarm re-prioritization.
"""

import logging
from typing import Dict, List
from config import settings
from intel.sentinel_apex_client import SentinelAIClient

# Configure high-authority logging
logger = logging.getLogger(__name__)

class ReasoningOrchestrator:
    def __init__(self):
        """
        Initializes the AI Reasoning Brain using the Sentinel-SDK.
        """
        self.ai_client = SentinelAIClient(api_key=settings.SENTINEL_APEX_KEY)
        self.processed_findings = set()

    async def analyze_and_retask(self, finding: Dict):
        """
        Evaluates a finding's potential for lateral movement and injects
        new, context-aware tasks back into the global swarm.
        """
        finding_id = f"{finding.get('type')}_{finding.get('url', finding.get('bucket', ''))}"
        
        if finding_id in self.processed_findings:
            return
        
        self.processed_findings.add(finding_id)

        # 1. Strategic AI Reasoning Phase
        analysis_prompt = f"""
        As a CyberDudeBivash Elite Analyst, evaluate this finding:
        Type: {finding.get('type')}
        Domain: {finding.get('domain')}
        Evidence: {finding.get('url') or finding.get('bucket')}
        
        Determine:
        1. Potential for lateral movement or privilege escalation.
        2. Specific related assets or endpoints to target next.
        3. Priority Level (0-10) for immediate swarm re-tasking.
        """
        
        # Connect to Sentinel APEX LLM Engine
        strategic_insight = await self.ai_client.get_reasoning(analysis_prompt)
        
        # 2. Autonomous Decision & Swarm Injection
        if strategic_insight.get('priority', 0) >= 8:
            logger.info(f"[GOD-MODE] Critical attack path identified: {strategic_insight.get('summary')}")
            await self._inject_autonomous_tasks(finding, strategic_insight.get('next_steps', []))

    async def _inject_autonomous_tasks(self, original_finding: Dict, next_steps: List[str]):
        """
        Delayed Import Strategy: Prevents Circular Dependency with scheduler_engine.
        """
        # FIX: Import inside the method to break the circular dependency chain
        from scheduler.scheduler_engine import run_distributed_recon

        for step in next_steps:
            target_domain = original_finding.get('domain')
            logger.info(f"[GOD-MODE] Injecting autonomous expansion task: {step} for {target_domain}")
            
            # Shard new specialized tasks based on AI reasoning with God-Mode priority
            run_distributed_recon.apply_async(
                args=[target_domain],
                kwargs={
                    'wordlist': 'wordlists/critical_paths.txt', 
                    'concurrency': 300
                },
                priority=10  # GOD-MODE HIGH PRIORITY
            )

# Singleton instance for platform-wide access
orchestrator = ReasoningOrchestrator()