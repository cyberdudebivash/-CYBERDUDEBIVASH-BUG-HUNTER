from analysis.asset_risk_engine import AssetRiskEngine


class AIReconAnalyzer:

    def __init__(self):

        self.risk_engine = AssetRiskEngine()

    async def analyze(self, domain, results):

        analysis = {
            "high_value_assets": [],
            "risk_scores": {},
        }

        subdomains = results.get("subdomains", [])
        endpoints = results.get("endpoints", [])

        for asset in subdomains + endpoints:

            score = self.risk_engine.calculate(asset)

            analysis["risk_scores"][asset] = score

            if score >= 80:
                analysis["high_value_assets"].append(asset)

        return analysis