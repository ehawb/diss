"""
Module based on 'Which trees are link graphs?' by Blass, Harary, Miller
"""
import networkx as nx
from neighborhood_utils.neighborhood_counter import count_neighborhoods, graph_neighborhoods
from itertools import chain, combinations


def get_neighborhood(graph, node):
    return graph.subgraph(list(graph.neighbors(node)))

def powerset(iterable):
    "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(1, len(s)+1))

def graph_in_scriptB(graph, scriptB):
    for B in scriptB:
        if nx.is_isomorphic(graph, B):
            return True
    return False

def check_B(link_graph, B):
    good_edges = []
    # print(f'              Checking B = {B}')
    edges = list(link_graph.edges)
    degree_B_vertices = [n for n, d in link_graph.degree() if d in B]
    for (u, v) in edges:
        if u in degree_B_vertices and v in degree_B_vertices:
            good_edges.append((u, v))
    return good_edges

def get_terms(link_graph, k, B):
    # get vertices in link graph of degree k
    vertices = [n for n, d in link_graph.degree() if d == k]
    # print(f'Vertices of degree {k}: {vertices}')
    # initialize max, min
    low, high = link_graph.order(), 0
    degree_B_vertices = [n for n, d in link_graph.degree() if d in B]
    for v in vertices:
        neighbors = list(link_graph.neighbors(v))
        num_good = 0
        good_neighbors = [n for n in neighbors if n in degree_B_vertices]
        if len(good_neighbors) < low:
            #print(f'Replacing previous min value of {low} with {len(good_neighbors)}')
            low = len(good_neighbors)
        if len(good_neighbors) > high:
            #print(f'Replacing previous max value of {high} with {len(good_neighbors)}')
            high = len(good_neighbors)
    # print(f'    Returning low of {low} and high of {high}')
    return low, high

def check_k(link_graph, k, possible_B, quick = False):
    total_check = True
    for B in possible_B:
        min_, max_ = get_terms(link_graph, k, B)
        #print(f'   For k = {k} got a min of {min_} and max {max_}')
        if k < min_ + max_:
            # continue to see if theorem holds
            if len(check_B(link_graph, B)) < 1:
                print(f'Failed for k = {k} with B = {B}')
                total_check = False
                if quick:
                    return False
    return total_check

def thm_one(link_graph, quick = False):
    total_check = True
    possible_k = set([d for n, d in link_graph.degree()])
    possible_B = list(powerset(list(range(1, link_graph.order()))))
    link_nbd_graphs = graph_neighborhoods(link_graph)
        # print(f'The link graph has {len(link_nbds)} neighborhoods.')
    for k in possible_k:
        # print(f'Checking k = {k} ... ... ... ')
        if not check_k(link_graph, k, possible_B, quick):
            total_check = False
            if quick:
                print(f'Quick check -- quitting now.')
                return False
    return total_check


