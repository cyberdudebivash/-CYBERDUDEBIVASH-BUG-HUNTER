class ReconAlertEngine:

    def __init__(self):

        self.previous_assets = set()

    async def process(self, domain, results):

        new_assets = []

        for sub in results.get("subdomains", []):

            if sub not in self.previous_assets:
                new_assets.append(sub)
                self.previous_assets.add(sub)

        if new_assets:

            print("[ALERT] New subdomains discovered")

            for a in new_assets:
                print(" -", a)

        endpoints = results.get("endpoints", [])

        if endpoints:

            print(f"[ALERT] {len(endpoints)} endpoints discovered on {domain}")