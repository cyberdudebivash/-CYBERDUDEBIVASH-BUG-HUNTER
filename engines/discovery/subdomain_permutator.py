class SubdomainPermutator:

    def __init__(self, domain):
        self.domain = domain

    def generate(self, subs):

        words = [
            "dev",
            "stage",
            "prod",
            "internal",
            "admin",
            "api",
            "beta",
            "test"
        ]

        generated = set()

        for sub in subs:
            prefix = sub.split(".")[0]

            for w in words:
                generated.add(f"{prefix}-{w}.{self.domain}")
                generated.add(f"{w}-{prefix}.{self.domain}")
                generated.add(f"{prefix}{w}.{self.domain}")

        return list(generated)