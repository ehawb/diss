from scipy.special import binom
from networkx import Graph, complete_graph
import itertools
import dill
from botparts.board import GameState, Board
from botparts.gametypes import Player

def read_2color_exoo_file(exoo_file, clique_orders, version = 'new'):
    with open(f'exoo_data/txt_files/{exoo_file}') as f:
        lines = f.readlines()
    f.close()
    num_vertices = len(lines)
    red_edges = []
    blue_edges = []
    red_clique_order, blue_clique_order = clique_orders
    for u in range(num_vertices):
        # print(u)
        neighbors = lines[u]
        # print(neighbors)
        for v in range(u+1, num_vertices):
            edge = (u, v)
            if neighbors[v] == '0':
                red_edges.append(edge)
            elif neighbors[v] == '1':
                blue_edges.append(edge)
                
    num_red = len(red_edges)
    num_blue = len(blue_edges)
    num_edges = num_red + num_blue
    should_be_edges = binom(num_vertices, 2)
    check = should_be_edges == num_edges
    if not check:
        print('Error somewhere...')
    else:
        if version == 'new':
            red_cliques = find_cliques(red_edges, red_clique_order)
            blue_cliques = find_cliques(blue_edges, blue_clique_order)
        elif version == 'old':
            red_cliques = find_cliques_old(red_edges, red_clique_order)
            blue_cliques = find_cliques_old(blue_edges, blue_clique_order)
        return {'red edges' : red_edges,
                'red cliques' : red_cliques,
                'blue edges' : blue_edges,
                'blue cliques' : blue_cliques}
    
def read_3color_exoo_file(exoo_file, clique_orders, version = 'new'):
    with open(f'exoo_data/txt_files/{exoo_file}') as f:
        lines = f.readlines()
    f.close()
    num_vertices = len(lines)
    red_edges = []
    blue_edges = []
    green_edges = []
    red_clique_order, blue_clique_order, green_clique_order = clique_orders
    for u in range(num_vertices):
        # print(u)
        neighbors = lines[u]
        # print(neighbors)
        for v in range(u+1, num_vertices):
            edge = (u, v)
            if neighbors[v] == '0':
                red_edges.append(edge)
            elif neighbors[v] == '1':
                blue_edges.append(edge)
            elif neighbors[v] == '2':
                green_edges.append(edge)

    num_red = len(red_edges)
    num_blue = len(blue_edges)
    num_green = len(green_edges)
    num_edges = num_red + num_blue + num_green
    should_be_edges = binom(num_vertices, 2)
    check = should_be_edges == num_edges
    if not check:
        print('Error somewhere...')
    else:
        if version == 'new':
            red_cliques = find_cliques(red_edges, red_clique_order)
            blue_cliques = find_cliques(blue_edges, blue_clique_order)
            green_cliques = find_cliques(green_edges, green_clique_order)
        elif version == 'old':
            red_cliques = find_cliques_old(red_edges, red_clique_order)
            blue_cliques = find_cliques_old(blue_edges, blue_clique_order)
            green_cliques = find_cliques_old(green_edges, green_clique_order)
        return {'red edges' : red_edges,
                'red cliques' : red_cliques,
                'blue edges' : blue_edges,
                'blue cliques' : blue_cliques,
                'green edges' : green_edges,
                'green cliques' : green_cliques}
    
def exoo_to_2color_gamestate(graph_order, clique_orders,
                      red_edges, red_cliques,
                      blue_edges, blue_cliques):
    player = Player.p1
    G = complete_graph(graph_order)
    board = Board(G)
    
    for red_edge in red_edges:
        board.graph.edges[red_edge]['color'] = 'red'
    for blue_edge in blue_edges:
        board.graph.edges[blue_edge]['color'] = 'blue'
    gamestate = GameState(board = board, next_player = player,
                          previous_state = None, recent_move = None,
                          clique_orders = clique_orders,
                          red_subgraph = Graph(red_edges), red_cliques = red_cliques,
                          blue_subgraph = Graph(blue_edges), blue_cliques = blue_cliques)
    return gamestate
    
def save_exoo(exoo_file, gamestate):
    """ Saves a gamestate created from Exoo coloring of a graph. This can be
    used as the starting point for some future game."""
    filename = exoo_file.strip('.txt')
    save_dir = f'exoo_data/pickles/{filename}_gamestate.pickle'
    with open(save_dir, 'wb') as file:
        dill.dump(gamestate, file)
    file.close()

def find_cliques(edge_list, clique_order):
    # based on update cliques methods in game logic...
    previously_searched_edges = []
    previously_searched_vertices = []
    cliques = []
    subgraph = Graph(edge_list)
    i = 0
    for edge in edge_list:
        u, v = edge
        previously_searched_edges.append(edge)
        # print(f'on edge {i+1}...')
        previously_searched_vertices.extend([u, v])
        u_neighbors = list(subgraph.neighbors(u))
        v_neighbors = list(subgraph.neighbors(v))
        # get a list of neighbors the vertices have in common
        common_neighbors = [vertex for vertex in u_neighbors if vertex in v_neighbors]
        # dealing with K3s as a separate case:
        for k in [3]:
            common_neighbors = [n for n in common_neighbors if ((u, n) not in previously_searched_edges and (n, u) not in previously_searched_edges)]
            common_neighbors = [n for n in common_neighbors if ((v, n) not in previously_searched_edges and (n, v) not in previously_searched_edges)]
            if (len(u_neighbors) < k-2) or (len(v_neighbors) < k-2):
                # if they individually don't have enough neighbors, no K3
                break
            if len(common_neighbors) < k-2:
                # if they don't share a common neighbor, no K3
                break
            for neighbor in common_neighbors:
                # if they have any common neighbors at all, all of those form
                # triangles.
                k3 = tuple(sorted((neighbor, u, v)))
                cliques.append(k3)
        for k in range(4, clique_order + 1):
            if (len(u_neighbors) < k-2) or (len(v_neighbors) < k-2):
                break
            if len(common_neighbors) < k-2:
                break
            # get a list of vertex subsets that would complete a clique with this edge
            vertex_subsets = list(itertools.combinations(common_neighbors, k-2))
            # get a list of possible edges between all common neighbors
            common_neighbors_possible_edges = list(
                itertools.combinations(common_neighbors, 2))
            # get a list of the possible edges that aren't actually there
            for edge in previously_searched_edges:
                # avoid duplicate searches
                u1, v1 = edge
                vertex_subsets = [subset for subset in vertex_subsets if not
                                  ((u1 in subset) and (v1 in subset))]
            # this will help narrow our search more (see below)
            not_edges = [edge for edge in common_neighbors_possible_edges if
                         edge not in subgraph.edges()]
            for edge in not_edges:
                u1, v1 = edge
                # remove some of those potential clique candidates
                vertex_subsets = [subset for subset in vertex_subsets if not
                                  ((u1 in subset) and (v1 in subset))]
                # remove trivial subsets
                vertex_subsets = [subset for subset in vertex_subsets if len(subset) > 1]

            # now we can hunt for cliques
            for subset in vertex_subsets:
                if subset in cliques:
                    clique_vertices = list(subset)
                    edge_vertices = [u, v]
                    clique = tuple(sorted(clique_vertices + edge_vertices))
                    cliques.append(clique)
                    break
                vertex_subset = list(subset)
                possible_edges = list(itertools.combinations(vertex_subset, 2))
                for edge in possible_edges:
                    if edge not in subgraph.edges():
                        break
                clique_vertices = list(subset)
                edge_vertices = [u, v]
                clique = tuple(sorted(clique_vertices + edge_vertices))
                cliques.append(clique)
                print(f'     {len(cliques)} cliques found so far. on edge {i+1} of {len(edge_list)}. searching K{k}')
        i +=1
    return cliques

def find_cliques_old(edge_list, clique_order):
    # based on update cliques methods in game logic...
    cliques = []
    print(edge_list)
    subgraph = Graph(edge_list)
    i = 0
    for edge in edge_list:
        print(f' ============ loop for {edge} ============')
        # input(f'time to look for {edge} cliques.')
        u, v = edge
        # print(f'on edge {i+1}...')
        u_neighbors = list(subgraph.neighbors(u))
        v_neighbors = list(subgraph.neighbors(v))
        # get a list of neighbors the vertices have in common
        common_neighbors = [vertex for vertex in u_neighbors if vertex in v_neighbors]
        # input(f'the edge {edge} has common neighbors: {common_neighbors}')
        # dealing with K3s as a separate case:
        for k in [3]:
            if (len(u_neighbors) < k-2) or (len(v_neighbors) < k-2):
                # if they individually don't have enough neighbors, no K3
                break
            if len(common_neighbors) < k-2:
                # if they don't share a common neighbor, no K3
                break
            for neighbor in common_neighbors:
                # if they have any common neighbors at all, all of those form
                # triangles.
                k3 = tuple(sorted((neighbor, u, v)))
                if k3 not in cliques:
                    cliques.append(k3)
        for k in range(4, clique_order + 1):
            if (len(u_neighbors) < k-2) or (len(v_neighbors) < k-2):
                # input(f'searching {edge}, not enough individual neighbors.')
                continue
            if len(common_neighbors) < k-2:
                # input(f'searching {edge}, not enough common neighbors.')
                continue
            # get a list of vertex subsets that would complete a clique with this edge
            vertex_subsets = list(itertools.combinations(common_neighbors, k-2))
            # get a list of possible edges between all common neighbors
            common_neighbors_possible_edges = list(
                itertools.combinations(common_neighbors, 2))
            # get a list of the possible edges that aren't actually there
            # this will help narrow our search more (see below)
            not_edges = [edge_ for edge_ in common_neighbors_possible_edges if
                         edge_ not in subgraph.edges()]
            for edge_ in not_edges:
                u1, v1 = edge_
                # remove some of those potential clique candidates
                vertex_subsets = [subset for subset in vertex_subsets if not
                                  ((u1 in subset) and (v1 in subset))]
                # remove trivial subsets
                vertex_subsets = [subset for subset in vertex_subsets if len(subset) > 1]
            # now we can hunt for cliques
            # input(f'searching for cliques of order {k} involving edge {edge} \n subsets: {vertex_subsets}')
            for subset in vertex_subsets:
                if subset in cliques:
                    clique_vertices = list(subset)
                    edge_vertices = [u, v]
                    clique = tuple(sorted(clique_vertices + edge_vertices))
                    if clique not in cliques:
                        cliques.append(clique)
                    # print(f'breaking after subset {subset} (working on {edge})')
                    continue
                vertex_subset = list(subset)
                possible_edges = list(itertools.combinations(vertex_subset, 2))
                for edge in possible_edges:
                    if edge not in subgraph.edges():
                        # input(f'breaking because {edge} is not an edge.')
                        continue
                clique_vertices = list(subset)
                edge_vertices = [u, v]
                clique = tuple(sorted(clique_vertices + edge_vertices))
                if clique not in cliques:
                    cliques.append(clique)
                print(f'     {len(cliques)} cliques found so far. on edge {i+1} of {len(edge_list)}. searching K{k}')
        i +=1
    return cliques

def pickle_2color_exoo(exoo_file, clique_orders, graph_order):
    graph_info = read_2color_exoo_file(exoo_file, clique_orders)
    red_edges = graph_info['red edges']
    blue_edges = graph_info['blue edges']
    red_cliques = graph_info['red cliques']
    blue_cliques = graph_info['blue cliques']
    
    gamestate = exoo_to_2color_gamestate(graph_order, clique_orders,
                                         red_edges, red_cliques,
                                         blue_edges, blue_cliques)
    save_exoo(exoo_file, gamestate)