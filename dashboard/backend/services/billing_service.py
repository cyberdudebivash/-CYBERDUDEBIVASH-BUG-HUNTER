class BillingService:

    plans = {

        "starter": {
            "domains": 3,
            "scans_per_day": 10
        },

        "pro": {
            "domains": 10,
            "scans_per_day": 50
        },

        "enterprise": {
            "domains": 100,
            "scans_per_day": 500
        }

    }

    def get_plan(self, plan):

        return self.plans.get(plan)