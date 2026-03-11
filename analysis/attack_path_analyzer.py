from collections import defaultdict


class AttackPathAnalyzer:

    def __init__(self):

        self.graph = defaultdict(set)

    def add_relationship(self, source, target):

        self.graph[source].add(target)

    def build_graph(self, results):

        domain = results.get("domain")

        subs = results.get("subdomains", [])
        endpoints = results.get("endpoints", [])
        urls = results.get("urls", [])

        for sub in subs:
            self.add_relationship(domain, sub)

        for url in urls:
            self.add_relationship(sub, url)

        for ep in endpoints:
            self.add_relationship(url, ep)

    def find_attack_paths(self, start):

        visited = set()
        paths = []

        def dfs(node, path):

            visited.add(node)
            path.append(node)

            if node not in self.graph:
                paths.append(path.copy())

            for neighbor in self.graph[node]:

                if neighbor not in visited:
                    dfs(neighbor, path)

            path.pop()

        dfs(start, [])

        return paths