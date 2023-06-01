import networkx as nx
from itertools import chain, combinations

def count_neighborhoods(graph):
    neighborhoods = {}
    i = 0
    for n in graph.nodes():
        i+=1
        # print(f"========= Checking node {n}, {i}/{len(graph.nodes())} ==========")
        neighbors = list(graph.neighbors(n))
        link = graph.subgraph(neighbors)
        if len(neighborhoods) == 0:
            neighborhoods[link] = 1
            continue
        num_neighborhoods = len(neighborhoods)
        result = is_new_neighborhood(link, neighborhoods)
        new = result[0]
        if new:
            # print('Found a new one!')
            neighborhoods[link] = 1
        else:
            # print('Already isomorphic to one in the list.')
            N = result[1]
            neighborhoods[N] += 1
    return neighborhoods

def is_new_neighborhood(link, neighborhood_dict):
    new = True
    for N in neighborhood_dict:
        if nx.is_isomorphic(link, N):
            return (False, N)
    return (True,)

def graph_neighborhoods(graph):
    gn = {}
    for n in graph.nodes():
        neighbors = list(graph.neighbors(n))
        link = graph.subgraph(neighbors)
        gn[n] = link
    return gn

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

def theorem_B_test(link_graph):
    link_nbds = list(count_neighborhoods(link_graph).keys())
    subsets = powerset(link_nbds)
    link_nbd_graphs = graph_neighborhoods(link_graph)
    # print(f'The link graph has {len(link_nbds)} neighborhoods.')
    for scriptB in subsets:
        # if it fails for any of them, then it doesn't work.
        if not check_scriptB(link_graph, scriptB, link_nbd_graphs):
            return False
    return True
        
def check_scriptB(link_graph, scriptB, link_nbd_graphs):
        B = []
        for H in scriptB:
            B += get_nodes_with_neighborhood(link_graph, H)
        C = []
        for b in B:
            C += list(link_graph.neighbors(b))
        C = list(set(C))
        C_dict = {node:link_nbd_graphs[node] for node in C}
        scriptC = list(C_dict.values())
        for Y in scriptC:
            check = check_Y(link_graph, Y, scriptC)
            if not check:
                print(f'Failed for ScriptB = {[graph6_string(B) for B in scriptB]}')
                return False
        return True
        
def check_Y(link_graph, Y, scriptC):
        check = False
        possible_u = get_nodes_with_neighborhood(link_graph, Y)
        edge_options = []
        for u in possible_u:
            edge_options += [(x, y) for (x, y) in link_graph.edges if u in (x, y)]
        for (y, z) in edge_options:
            if y in possible_u:
                # check z
                z_neighborhood = link_graph.subgraph(list(link_graph.neighbors(z)))
                for H in scriptC:
                    if nx.is_isomorphic(H, z_neighborhood):
                        return True
            if z in possible_u:
                y_neighborhood = link_graph.subgraph(list(link_graph.neighbors(y)))
                for H in scriptC:
                    if nx.is_isomorphic(H, y_neighborhood):
                        return True
        return False

def check_scriptB_BC(link_graph, scriptB, link_nbd_graphs):
        B = []
        for H in scriptB:
            B += get_nodes_with_neighborhood(link_graph, H)
        C = []
        for b in B:
            C += list(link_graph.neighbors(b))
        C = list(set(C))
        C_dict = {node:link_nbd_graphs[node] for node in C}
        scriptC = list(C_dict.values())
        scriptC_not_B = []
        for Y in scriptC:
            in_scriptB = False
            for Z in scriptB:
                if nx.is_isomorphic(Y, Z):
                    in_scriptB = True
            if not in_scriptB:
                scriptC_not_B.append(Y)
        for Y in scriptC_not_B:
            check = check_Y(link_graph, Y, scriptC_not_B)
            if not check:
                print(f'Failed for ScriptB = {[graph6_string(B) for B in scriptB]}')
                return False
        return True

def get_other_cliques(link_graph, k, B):
    # Get cliques of order k in a graph.
    cliques = []
    for s in combinations(link_graph.nodes, k):
        if len([b for b in B if b not in s]) == 0: 
            continue
        if nx.is_isomorphic(nx.subgraph(link_graph, s), nx.complete_graph(k)):
            cliques.append(s)
    return cliques

def neighborhood_intersection(link_graph, vertices):
    common_neighbors = list(link_graph.nodes)
    for v in vertices:
        neighbors = list(link_graph.neighbors(v))
        common_neighbors = [n for n in common_neighbors if n in neighbors]
    return common_neighbors

def cliques_good(link_graph, k, B):
    other_cliques = get_other_cliques(link_graph, k, B)
    if len(other_cliques) == 0:
        print("No other cliques, so it's boring...")
    B_neighbor_graph = nx.subgraph(link_graph, neighborhood_intersection(link_graph, B))
    for c in other_cliques:
        if nx.is_isomorphic(nx.subgraph(link_graph, neighborhood_intersection(link_graph, c)),
                            B_neighbor_graph):
            return False
    return True
    
def theorem_BC(link_graph):
    BC_applies = False
    link_nbds = list(count_neighborhoods(link_graph).keys())
    subsets = powerset(link_nbds)
    link_nbd_graphs = graph_neighborhoods(link_graph)
    # print(f'The link graph has {len(link_nbds)} neighborhoods.')
    for scriptB in subsets:
        # if it fails for any of them, then it doesn't work.
        B = []
        for H in scriptB:
            B += get_nodes_with_neighborhood(link_graph, H)
        k = len(B)
        if nx.is_isomorphic(nx.subgraph(link_graph, B), nx.complete_graph(k)):
            # Theorem BC might apply
            if cliques_good(link_graph, k, B):
                print(f'The assumptions of Theorem BC are satisfied when B = {B}')
                BC_applies = True
                if not check_scriptB_BC(link_graph, scriptB, link_nbd_graphs):
                    return False
    if not BC_applies:
        print('The assumptions of Theorem BC were not satisfied.')
    return True

def graph6_string(graph):
    g6 = nx.to_graph6_bytes(graph)
    graph6_string = str(g6)[12:-3]
    return graph6_string