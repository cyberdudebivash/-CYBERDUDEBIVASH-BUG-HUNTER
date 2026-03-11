import networkx as nx


class AssetGraphEngine:

    def __init__(self):
        self.graph = nx.Graph()

    def add_domain(self, domain):
        self.graph.add_node(domain, type="domain")

    def add_subdomain(self, sub, domain):
        self.graph.add_node(sub, type="subdomain")
        self.graph.add_edge(domain, sub)

    def add_ip(self, sub, ip):
        self.graph.add_node(ip, type="ip")
        self.graph.add_edge(sub, ip)

    def visualize(self):
        return self.graph