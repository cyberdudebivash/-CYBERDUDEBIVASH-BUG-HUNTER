class AssetRiskEngine:

    def __init__(self):

        self.high_risk_keywords = [
            "admin",
            "internal",
            "dev",
            "test",
            "staging",
            "api",
            "auth",
        ]

    def calculate(self, asset):

        score = 10

        for keyword in self.high_risk_keywords:

            if keyword in asset.lower():
                score += 20

        if "/api/" in asset:
            score += 15

        if "login" in asset:
            score += 15

        return min(score, 100)