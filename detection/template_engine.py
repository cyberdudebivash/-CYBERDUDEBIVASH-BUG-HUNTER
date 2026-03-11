import re


class TemplateEngine:

    def __init__(self):

        self.templates = []

    def load_templates(self, templates):

        self.templates = templates

    async def scan(self, urls):

        findings = []

        for url in urls:

            for template in self.templates:

                pattern = template.get("pattern")

                if re.search(pattern, url):

                    findings.append({
                        "url": url,
                        "issue": template.get("name"),
                        "severity": template.get("severity"),
                    })

        return findings