import networkx as nx

class Annulus:
    def __init__(self, n):
        self.n = n
        self.graph = None
        self.del_ = None
    
    def graph_construction(self):
        cycle = nx.cycle_graph(self.n)
        self.del_ = nx.disjoint_union(cycle, cycle)
        graph = nx.disjoint_union(cycle, cycle)
        outer_nodes = list(range(self.n)) + [0] # back to start
        inner_nodes = list(range(self.n, 2*self.n))
        new_edges = []
        for i in range(self.n):
            # print(f'for i = {i} we have inner node {inner_nodes[i]} joined with outer nodes {outer_nodes[i]} and {outer_nodes[i+1]}')
            new_edges += [(outer_nodes[i], inner_nodes[i]), (outer_nodes[i+1], inner_nodes[i])]
        graph.add_edges_from(new_edges)
        self.graph = graph
        return graph
    

