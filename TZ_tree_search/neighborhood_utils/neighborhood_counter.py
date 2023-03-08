import networkx as nx

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