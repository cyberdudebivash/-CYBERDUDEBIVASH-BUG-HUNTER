import yaml
import fnmatch


class ProgramScopeManager:

    def __init__(self, config_file="programs.yaml"):
        self.config_file = config_file
        self.programs = {}

        self.load()

    def load(self):

        with open(self.config_file) as f:
            data = yaml.safe_load(f)

        self.programs = data.get("programs", {})

    def get_all_targets(self):

        targets = []

        for program, pdata in self.programs.items():

            domains = pdata.get("domains", [])

            for d in domains:
                targets.append({
                    "program": program,
                    "domain": d
                })

        return targets

    def in_scope(self, domain):

        for program, pdata in self.programs.items():

            patterns = pdata.get("domains", [])

            for pattern in patterns:

                if fnmatch.fnmatch(domain, pattern):
                    return True

        return False