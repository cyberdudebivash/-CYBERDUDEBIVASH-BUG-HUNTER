import requests


class SentinelApexClient:

    def __init__(self):

        self.api = "https://sentinel.cyberdudebivash.com/api"

    def check_ioc(self, value):

        try:

            r = requests.get(
                f"{self.api}/ioc",
                params={"value": value},
                timeout=5
            )

            return r.json()

        except Exception:

            return None

    def enrich_assets(self, assets):

        intel = []

        for asset in assets:

            result = self.check_ioc(asset)

            if result:
                intel.append(result)

        return intel