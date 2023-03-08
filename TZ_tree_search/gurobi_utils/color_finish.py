import itertools
import networkx as nx
from gurobi_subgraphs import edge_colored_graph, finish_check, print_board

def edge_options(edge, colors):
    options = list(itertools.product([edge], colors))
    return options

def finish_options(edges, colors):
    all_options = []
    for e in edges:
        all_options.append(edge_options(e, colors))
    final = list(itertools.product(*all_options))
    return final

def get_finishes(graph):
    n = graph.order()
    missing_edges = [e for e in nx.complete_graph(n).edges if e not in graph.edges]
    num_missing = len(missing_edges)
    colors = ['red', 'blue']
    finishes = finish_options(missing_edges, colors)
    return finishes

def apply_finish(graph, finish):
    red_edges = [(u, v) for (u, v) in graph.edges if graph[u][v]['color'] == 'red']
    blue_edges = [(u, v) for (u, v) in graph.edges if graph[u][v]['color'] == 'blue']
    print(f'      Applying finsh: {finish}')
    for e in finish:
        u, v = e[0]
        color = e[1]
        print(f'Coloring edge {(u, v)} {color}')
        if color == 'red':
            red_edges.append((u, v))
        else:
            blue_edges.append((u, v))
    n = graph.order()
    colored_graph = edge_colored_graph(n, red_edges, blue_edges)
    print(f'Returning applied finish graph with red edges {red_edges}')
    return colored_graph

def finish_coloring(graph):
    finish = get_finishes(graph)
    finished_colorings = []
    for f in finish:
        print(f'Need to apply finish {f}')
        colored_graph = apply_finish(graph, f)
        finished_colorings.append(colored_graph)
    print(f'Returning {len(finished_colorings)} finished colorings.')
    return finished_colorings

def finish_coloring_dict(graph):
    finish = get_finishes(graph)
    finished_colorings = {}
    for f in finish:
        colored_graph = apply_finish(graph, f)
        finished_colorings[f] = colored_graph
    return finished_colorings

def get_edge_colors(graph):
    red_edges = [(u, v) for (u, v) in list(graph.edges) if graph[u][v]['color'] == 'red']
    blue_edges = [(u, v) for (u, v) in list(graph.edges) if graph[u][v]['color'] == 'blue']
    return red_edges, blue_edges

def check_finishes(finished_colorings, forbidden_subgraphs):
    i = 0
    good = [] # keep track of good colorings
    required_checks = len(forbidden_subgraphs) # number of checks to pass test
    for G in finished_colorings:
        print(f'Checking graph {i+1} of {len(finished_colorings)}.....................................................................')
        i +=1
        check = get_edge_colors(G)
        print(f'    Red edges: {check[0]}')
        print(f'    Blue edges: {check[1]}')
        passed_checks = 0
        for H in forbidden_subgraphs:
            if finish_check(G, H):
                print('                                                Passed a check!')
                passed_checks += 1
        if passed_checks >= required_checks:
            print("""
                  ===========================
                  ===========================
                  ===========================
                  ====graph passed checks!===
                  ===========================
                  ===========================
                  ===========================
                  ===========================
                  ===========================
                  """
                  )
            good.append(G)
    return good

def check_finishes_dict(finished_colorings, forbidden_subgraphs):
    i = 0
    good = {} # keep track of good colorings
    required_checks = len(forbidden_subgraphs) # number of checks to pass test
    for f in finished_colorings:
        print(f'Checking graph {i+1} of {len(finished_colorings)}.....................................................................')
        i +=1
        G = finished_colorings[f]
        check = get_edge_colors(G)
        print(f'    Red edges: {check[0]}')
        print(f'    Blue edges: {check[1]}')
        passed_checks = 0
        for H in forbidden_subgraphs:
            if finish_check(G, H):
                print('                                                Passed a check!')
                passed_checks += 1
        if passed_checks >= required_checks:
            print("""
                  ===========================
                  ===========================
                  ===========================
                  ====graph passed checks!===
                  ===========================
                  ===========================
                  ===========================
                  ===========================
                  ===========================
                  """
                  )
            good[f] = G
            
    return good

def complete_coloring(graph, forbidden_subgraphs):
    finished_colorings = finish_coloring(graph)
    good_finishes = check_finishes(finished_colorings, forbidden_subgraphs)
    return good_finishes

def complete_coloring_return_finishes(graph, forbidden_subgraphs):
    finished_colorings = finish_coloring_dict(graph)
    good_finishes = check_finishes_dict(finished_colorings, forbidden_subgraphs)
    return good_finishes

def edge_comparison(new_G, old_G):
    old_red_edges = [(u, v) for (u, v) in old_G.edges if old_G[u][v]['color'] == 'red']
    old_blue_edges = [(u, v) for (u, v) in old_G.edges if old_G[u][v]['color'] == 'blue']
    new_red_edges = [(u, v) for (u, v) in new_G.edges if new_G[u][v]['color'] == 'red']
    new_blue_edges = [(u, v) for (u, v) in new_G.edges if new_G[u][v]['color'] == 'blue']
    added_red = [e for e in new_red_edges if e not in old_red_edges]
    added_blue = [e for e in new_blue_edges if e not in old_blue_edges]
    return added_red, added_blue

def extend_coloring(graph, forbidden_subgraphs, extension_order):
    red_edges = [(u, v) for (u, v) in graph.edges if graph[u][v]['color'] == 'red']
    blue_edges = [(u, v) for (u, v) in graph.edges if graph[u][v]['color'] == 'blue']
    extended_graph = edge_colored_graph(extension_order, red_edges, blue_edges)
    finished_colorings = finish_coloring(extended_graph)
    good_finishes = check_finishes(finished_colorings, forbidden_subgraphs)
    return good_finishes

def extend_coloring_return_finishes(graph, forbidden_subgraphs, extension_order):
    red_edges = [(u, v) for (u, v) in graph.edges if graph[u][v]['color'] == 'red']
    blue_edges = [(u, v) for (u, v) in graph.edges if graph[u][v]['color'] == 'blue']
    extended_graph = edge_colored_graph(extension_order, red_edges, blue_edges)
    finished_colorings = finish_coloring_dict(extended_graph)
    good_finishes = check_finishes_dict(finished_colorings, forbidden_subgraphs)
    return good_finishes