"""
Module based on a generalization of
'Which trees are link graphs?' by Blass, Harary, Miller
"""

import networkx as nx
from neighborhood_utils.neighborhood_counter import count_neighborhoods, graph_neighborhoods
from itertools import chain, combinations

def get_nodes_with_neighborhood(graph, neighborhood):
    nodes = []
    graph_nbds = graph_neighborhoods(graph)
    for n in graph.nodes():
        node_neighborhood = graph_nbds[n]
        if nx.is_isomorphic(node_neighborhood, neighborhood):
            nodes.append(n)
    return nodes

def powerset(iterable):
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def graph_in_scriptB(graph, scriptB):
    for B in scriptB:
        if nx.is_isomorphic(graph, B):
            return True
    return False

def get_terms(link_graph, k, scriptB):
    vertices = [n for n, d in link_graph.degree() if d == k]
    low, high = link_graph.order(), 0
    for v in vertices:
        neighbors = list(link_graph.neighbors(v))
        num_good = 0
        for u in neighbors:
            neighbor_link = link_graph.subgraph(list(link_graph.neighbors(u)))
            if graph_in_scriptB(neighbor_link, scriptB):
                num_good +=1
        if num_good < low:
            low = num_good
        if num_good > high:
            high = num_good
    return low, high

def check_scriptB(link_graph, scriptB):
    edges = list(link_graph.edges)
    for (u, v) in edges:
        u_link = link_graph.subgraph(list(link_graph.neighbors(u)))
        v_link = link_graph.subgraph(list(link_graph.neighbors(v)))
        if graph_in_scriptB(u_link, scriptB) and graph_in_scriptB(v_link, scriptB):
            return True
        
def thm_one_gen(link_graph, quick = False):
    total_result = True
    possible_k = set([d for n, d in link_graph.degree()])
    link_nbds = list(count_neighborhoods(link_graph).keys())
    subsets = list(powerset(link_nbds))
    link_nbd_graphs = graph_neighborhoods(link_graph)
    for k in possible_k:
        for scriptB in subsets:
            min_, max_ = get_terms(link_graph, k, scriptB)
            if k < min_ + max_:
                if not check_scriptB(link_graph, scriptB):
                    strings = [graph6_string(B) for B in scriptB]
                    print(f'Failed for k = {k} with {len(scriptB)} Script B graphs: {strings}')
                    total_result = False
                    if quick:
                        print('Quick check -- quitting now.')
                        return False
    return total_result

def graph6_string(graph):
    g6 = nx.to_graph6_bytes(graph)
    graph6_string = str(g6)[12:-3]
    return graph6_string