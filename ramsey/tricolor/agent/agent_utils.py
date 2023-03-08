import networkx as nx
from copy import deepcopy
import itertools

def colored_edge_list(graph):
    edges = list(graph.edges)
    red_ind, blue_ind, green_ind = (0,), (1,), (2,)
    red_edges = [edge + red_ind for edge in edges]
    blue_edges = [edge + blue_ind for edge in edges]
    green_edges = [edge + green_ind for edge in edges]
    all_edges = red_edges + blue_edges + green_edges
    
    return all_edges

def get_indices(sub_edges, host_edges):
    indices = [host_edges.index(sub_edge) for sub_edge in sub_edges]
    return indices

def get_edges(host_edges, indices):
    sub_edges = [host_edges[ind] for ind in indices]
    return sub_edges

def get_priors(priors, indices):
    priors = [priors[ind] for ind in indices]
    return priors

def host_edge_list(host_graph_order):
    host_graph = nx.complete_graph(host_graph_order)
    host_edges = colored_edge_list(host_graph)
    return host_edges

def ends_game(edge, game):
    """ Returns a boolean indicating whether coloring a particular edge with the given
    color would end the game. """
    state = deepcopy(game)
    # print(f'checking in select branch if {edge} will end game.')
    colors = {0: 'red', 1: 'blue', 2: 'green'}
    color_ind = edge[2]
    color = colors[color_ind]
    if color == 'red':
        clique_order = state.red_clique_order
        prev_edges = list(state.red_subgraph.edges())
        prev_cliques = state.red_cliques
    elif color == 'blue':
        clique_order = state.blue_clique_order
        prev_edges = list(state.blue_subgraph.edges())
        prev_cliques = state.blue_cliques
    elif color == 'green':
        clique_order = state.green_clique_order
        prev_edges = list(state.green_subgraph.edges())
        prev_cliques = state.green_cliques
    new_edge = (edge[0], edge[1])
    if len(prev_edges) == 0:
        return False
    cliques = check_monochromatic_cliques(clique_order, new_edge,
                                          prev_edges, prev_cliques)
    # print(f'info found: \n cliques: {cliques} \n clique order: {clique_order}')    
    if len(cliques) == 0:
        # no cliques
        # print('no cliques at all.')
        return False
    largest_clique = max(cliques, key = len)
    if len(largest_clique) >= clique_order:
        # print(f'the edge will form a clique too large: {largest_clique}')
        # input('returning true for end game. [enter]')
        return True
    else:
        # print('returning false.')
        return False
    
def check_monochromatic_cliques(clique_order, new_edge, 
                                prev_edges, prev_cliques):
    """Check if a particular move in a particular color results in a 
    monochromatic clique of the relevant size."""
    #### turn the move into something that can be worked with.
    u, v = new_edge
    subgraph_edges = [new_edge] + prev_edges
    graph = nx.Graph(subgraph_edges)
    # print(f'checking cliques after coloring {edge} {color}')
    ### get the info we need for relevant color
    max_k = clique_order
    prior_cliques = prev_cliques
    #### initialize list of actual cliques:
    cliques = []
    #### if there isn't a monochromatic subgraph,
    if graph is None:
        #### then there definitely aren't any cliques.
        return cliques
    #### now get a list of neighbors that u and v have in common.
    u_neighbors = list(graph.neighbors(u))
    v_neighbors = list(graph.neighbors(v))
    common_neighbors = [vertex for vertex in u_neighbors 
                            if vertex in v_neighbors]
    # print(f'u neighbors: {u_neighbors}')
    # print(f'v neighbors: {v_neighbors}')
    #### iterate through all of the different possible clique orders:
    #### k = 3 needs to be handled separately!
    for k in [3]:
        if (len(u_neighbors) < k-2) or (len(v_neighbors) < k-2):
            break
        if len(common_neighbors) < k-2:
            # print(f'not enough common neighbors.')
            break
        ### if two vertices that have recently been connected by an edge
        ### share a common neighbor, then there is definitely a K3 formed.
        for neighbor in common_neighbors:
            K3 = tuple(sorted((neighbor, u, v)))
            cliques.append(K3)
            # print(f'appended K3: {K3}')
    for k in range(4, max_k+1):
        #### (remember that max_k is the order of the monochromatic clique
        #### we're trying to avoid in the original problem)
        # print(f'checking k = {k}')
        # print(f'{u} neighbors: {u_neighbors}')
        # print(f'{v} neighbors: {v_neighbors}')
        #### if there aren't enough neighbors, break
        if (len(u_neighbors) < k-2) or (len(v_neighbors) < k-2):
            break
        ##### get a list of common neighbors shared between the edges
        # print(f'neighbors {u} and {v} have in common:')
        # print(f'common neighbors: {common_neighbors}')
        #### if there aren't enough common neighbors, break
        if len(common_neighbors) < k-2:
            # print(f'not enough common neighbors.')
            break
        vertex_subsets = list(itertools.combinations(common_neighbors, k-2))
        #### if an edge doesn't exist between two common neighbors,
        ##### we don't need to consider those neighbors
        common_neighbors_possible_edges = list(
            itertools.combinations(common_neighbors, 2))
        # print(f'common neighbors for {u} and {v}: {common_neighbors}')
        # print(f'possible edges: {common_neighbors_possible_edges}')
        not_edges = [edge for edge in common_neighbors_possible_edges
                     if edge not in graph.edges()]
        # print(f'not edges: {not_edges}')
        for edge in not_edges:
            u1, v1 = edge
            vertex_subsets = [subset for subset in vertex_subsets if not 
                              ((u1 in subset) and (v1 in subset))]
            # print(f'vertex_subsets: {vertex_subsets}')
            vertex_subsets = [subset for subset in vertex_subsets if len(subset) > 1]
            # print(f'vertex subsets: {vertex_subsets}')
        #### now we have a list of potential cliques.
        #### check if each tuple forms a clique
        for subset in vertex_subsets:
            # print(f'checking {color} {subset} for clique.')
            #### if we have prior cliques to work with,
            if prior_cliques is not None:
                #### check those first.
                if subset in prior_cliques:
                    clique_vertices = list(subset)
                    edge_vertices = [u, v]
                    clique = tuple(sorted(clique_vertices + edge_vertices))
                    cliques.append(clique)
                    break
            #### otherwise, convert the tuple to a list
            vertex_subset = list(subset)
            #### get a list of all possible edges among the tuple
            possible_edges = list(itertools.combinations(vertex_subset, 2))
            #### see if the edges are in the graph
            for edge in possible_edges:
                #### if not, no clique
                if edge not in graph.edges():
                    break
            #### otherwise, get the vertices cleaned up
            clique_vertices = list(subset)
            edge_vertices = [u, v]
            clique = tuple(sorted(clique_vertices + edge_vertices))
            # print(f' adding {color} clique: {clique}')
            # and add the clique to the list
            cliques.append(clique)
    # print(f'returning cliques: {cliques}')
    return cliques