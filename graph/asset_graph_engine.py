from collections import defaultdict


class AssetGraphEngine:

    def __init__(self):

        self.graph = defaultdict(set)

    async def ingest_results(self, domain, results):

        subs = results.get("subdomains", [])
        urls = results.get("urls", [])
        endpoints = results.get("endpoints", [])

        for sub in subs:
            self.graph[domain].add(sub)

        for url in urls:
            self.graph["urls"].add(url)

        for ep in endpoints:
            self.graph["endpoints"].add(ep)

    def get_assets(self, node):

        return list(self.graph.get(node, []))

    def stats(self):

        return {
            "domains": len(self.graph)
        }