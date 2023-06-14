import networkx as nx
import matplotlib.pyplot as plt

def construct_cyclic_cayley_graph(n, S):
    """n is the order of the graph; S is a set of generators."""
    vertices = list(range(n))
    edges = []
    for v in vertices:
        for s in S:
            neighbor = (v + s) % n
            if v < neighbor:
                edges.append((v, neighbor))
    return nx.Graph(edges)

