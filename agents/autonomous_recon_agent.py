from analysis.ai_recon_analyzer import AIReconAnalyzer
from core.recon_pipeline import ReconPipeline


class AutonomousReconAgent:

    def __init__(self):

        self.analyzer = AIReconAnalyzer()

    async def analyze_and_expand(self, domain):

        pipeline = ReconPipeline(domain)

        results = await pipeline.run()

        analysis = await self.analyzer.analyze(domain, results)

        high_value = analysis.get("high_value_assets", [])

        next_targets = []

        for asset in high_value:

            if "api" in asset or "admin" in asset:
                next_targets.append(asset)

        return {
            "results": results,
            "next_targets": next_targets
        }

    async def autonomous_cycle(self, target):

        queue = [target]

        processed = set()

        while queue:

            domain = queue.pop(0)

            if domain in processed:
                continue

            processed.add(domain)

            outcome = await self.analyze_and_expand(domain)

            queue.extend(outcome["next_targets"])