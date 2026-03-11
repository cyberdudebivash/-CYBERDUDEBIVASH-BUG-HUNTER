import aiohttp


class TemplateEngine:

    def __init__(self, templates):
        self.templates = templates

    async def scan(self, url):

        findings = []

        async with aiohttp.ClientSession() as session:

            for tpl in self.templates:

                target = url + tpl["path"]

                try:
                    async with session.get(target, timeout=10) as r:
                        text = await r.text()

                        if tpl["match"] in text:
                            findings.append({
                                "url": target,
                                "template": tpl["id"],
                                "severity": tpl["severity"]
                            })

                except:
                    pass

        return findings