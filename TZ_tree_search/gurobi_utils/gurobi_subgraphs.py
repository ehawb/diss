import gurobipy as gp
from gurobipy import quicksum
from gurobipy import GRB
from math import factorial
import numpy as np
import scipy.sparse as sp
import networkx as nx
import matplotlib.pyplot as plt
import time
import random
import string

def model_id(length = 12, chars = string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(length))

                          
def finish_check(G, H):
    n = G.order()
    j_n = np.ones(n)
    m = H.order()
    j_m = np.ones(m)
    date_time = time.strftime("%H_%M_%S")
    model_string = model_id()
    model_name = f'Subgraph{date_time}_{model_string}'
    with gp.Model(model_name) as subg:
        print(f'Running model {model_name}')
        subg = gp.Model(model_name)
        X = subg.addMVar((m, n), vtype = GRB.BINARY, name = 'map')
        subg.setObjective(sum(j_n[i] * j_m @ X[:, i] for i in range(n)), GRB.MINIMIZE)
        # each column should sum to at most 1
        for i in range(n):
            subg.addConstr(sum(X[:, i]) <= 1, name = f'Col {i} sum')
        # each row should sum to exactly 1    
        for i in range(m):
            subg.addConstr(sum(X[i, :]) == 1, name = f'Row {i} sum')
        # edge weight constraints
        Kn = nx.complete_graph(n)
        not_G_edges = [e for e in Kn.edges if e not in G.edges]
        print(f'n = {n}, m = {m}')
        for (u_i, u_j) in H.edges:
            for (v_r, v_s) in not_G_edges:
                subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v1')
                subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v2')
        # more edge weight constraints
        for (u_i, u_j) in H.edges:
            for (v_r, v_s) in G.edges:
                if H[u_i][u_j]['color'] != G[v_r][v_s]['color']:
                    subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} color')
                    subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_s, v_r)} color')
        subg.optimize()
    if subg.SolCount < 1:
        # no solutions means H isn't a subgraph of G, which is good in this context
        return True
    else:
        # otherwise, the finished coloring fails
        return False
        
def subgraph_check(G, H):
    n = G.order()
    j_n = np.ones(n)
    m = H.order()
    j_m = np.ones(m)
    
    subg = gp.Model('Subgraph')
    X = subg.addMVar((m, n), vtype = GRB.BINARY, name = 'map')
    subg.setObjective(sum(j_n[i] * j_m @ X[:, i] for i in range(n)), GRB.MINIMIZE)
    # each column should sum to at most 1
    for i in range(n):
        subg.addConstr(sum(X[:, i]) <= 1, name = f'Col {i} sum')
    # each row should sum to exactly 1    
    for i in range(m):
        subg.addConstr(sum(X[i, :]) == 1, name = f'Row {i} sum')
    # edge weight constraints
    Kn = nx.complete_graph(n)
    not_G_edges = [e for e in Kn.edges if e not in G.edges]
    for (u_i, u_j) in H.edges:
        for (v_r, v_s) in not_G_edges:
            subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v1')
            subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v2')
    # more edge weight constraints
    for (u_i, u_j) in H.edges:
        for (v_r, v_s) in G.edges:
            if H[u_i][u_j]['color'] != G[v_r][v_s]['color']:
                subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} color')
                subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_s, v_r)} color')
    subg.optimize()
    
def subgraph_check_result(G, H):
    n = G.order()
    j_n = np.ones(n)
    m = H.order()
    j_m = np.ones(m)
    
    subg = gp.Model('Subgraph')
    X = subg.addMVar((m, n), vtype = GRB.BINARY, name = 'map')
    subg.setObjective(sum(j_n[i] * j_m @ X[:, i] for i in range(n)), GRB.MINIMIZE)
    # each column should sum to at most 1
    for i in range(n):
        subg.addConstr(sum(X[:, i]) <= 1, name = f'Col {i} sum')
    # each row should sum to exactly 1    
    for i in range(m):
        subg.addConstr(sum(X[i, :]) == 1, name = f'Row {i} sum')
    # edge weight constraints
    Kn = nx.complete_graph(n)
    not_G_edges = [e for e in Kn.edges if e not in G.edges]
    for (u_i, u_j) in H.edges:
        for (v_r, v_s) in not_G_edges:
            subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v1')
            subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v2')
    # more edge weight constraints
    for (u_i, u_j) in H.edges:
        for (v_r, v_s) in G.edges:
            if H[u_i][u_j]['color'] != G[v_r][v_s]['color']:
                subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} color')
                subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_s, v_r)} color')
    subg.optimize()
    if subg.SolCount == 0:
        return False
    else:
        return True
def basic_isomorphism_check_result(G, H):
    n = G.order()
    j_n = np.ones(n)
    m = H.order()
    j_m = np.ones(m)
    with gp.Env(empty = True) as env:
        env.setParam('OutputFlag', 0)
        env.start()
        with gp.Model('Subgraph', env=env) as subg:
            X = subg.addMVar((m, n), vtype = GRB.BINARY, name = 'map')
            subg.setObjective(sum(j_n[i] * j_m @ X[:, i] for i in range(n)), GRB.MINIMIZE)
            # Column restraints
            for i in range(n):
                subg.addConstr(sum(X[:, i]) == 1, name = f'Col{i} sum')
            # Row constraints
            for i in range(m):
                subg.addConstr(sum(X[i, :]) == 1, name = f'Row {i} sum')
            K_n = nx.complete_graph(n)
            not_G_edges = [e for e in K_n.edges if e not in G.edges]
            for (u_i, u_j) in list(H.edges):
                for (v_r, v_s) in not_G_edges:
                    subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v1')
                    subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v2')
            subg.optimize()
            if subg.SolCount == 0:
                return False
            else:
                return True

def get_restraints(G, H, solution):
    mapping = np.array(solution)
    n = G.order()
    m = H.order()
    mapping = mapping.reshape((m, n))
    
    maps = []
    for i in range(m):
        for j in range(n):
            if mapping[i][j] == 1:
                maps.append((i, j))
    map_dict = {}
    for map_ in maps:
        u, u_prime = map_
        map_dict[u] = u_prime
    return mapping    

def all_subgraph_check(G, H):
    n = G.order()
    j_n = np.ones(n)
    m = H.order()
    j_m = np.ones(m)
    
    subg = gp.Model('Subgraph')
    X = subg.addMVar((m, n), vtype = GRB.BINARY, name = 'map')
    subg.setObjective(sum(j_n[i] * j_m @ X[:, i] for i in range(n)), GRB.MINIMIZE)
    # each column should sum to at most 1
    for i in range(n):
        subg.addConstr(sum(X[:, i]) <= 1, name = f'Col {i} sum')
    # each row should sum to exactly 1    
    for i in range(m):
        subg.addConstr(sum(X[i, :]) == 1, name = f'Row {i} sum')
    # edge weight constraints
    Kn = nx.complete_graph(n)
    not_G_edges = [e for e in Kn.edges if e not in G.edges]
    for (u_i, u_j) in H.edges:
        for (v_r, v_s) in not_G_edges:
            subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v1')
            subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v2')
    # more edge weight constraints
    for (u_i, u_j) in H.edges:
        for (v_r, v_s) in G.edges:
            if H[u_i][u_j]['color'] != G[v_r][v_s]['color']:
                subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} color')
                subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_s, v_r)} color')
    subg.optimize()
    total_maps = 0
    all_maps = []
    while subg.SolCount > 0:
        mapping = get_restraints(G, H, subg.X)
        total_maps +=1
        pairs = []
        for i in range(m):
            for j in range(n):
                if mapping[i][j] == 1:
                    pairs.append((i, j))
        print(pairs)
        all_maps.append(pairs)
        subg.addConstr(sum((X[i, j]) for (i, j) in pairs) <= m-1, name = 'Eliminating previous solution {total_maps}')
        subg.optimize()
    print(f'Found {total_maps} solutions in all.')            
    return all_maps 

def all_subgraph_check_plain(G, H):
    n = G.order()
    j_n = np.ones(n)
    m = H.order()
    j_m = np.ones(m)
    with gp.Env(empty = True) as env:
        env.setParam('OutputFlag', 0)
        env.start()
        with gp.Model('Subgraph', env=env) as subg:
            X = subg.addMVar((m, n), vtype = GRB.BINARY, name = 'map')
            subg.setObjective(sum(j_n[i] * j_m @ X[:, i] for i in range(n)), GRB.MINIMIZE)
            # each column should sum to at most 1
            for i in range(n):
                subg.addConstr(sum(X[:, i]) <= 1, name = f'Col {i} sum')
            # each row should sum to exactly 1    
            for i in range(m):
                subg.addConstr(sum(X[i, :]) == 1, name = f'Row {i} sum')
            # edge weight constraints
            Kn = nx.complete_graph(n)
            not_G_edges = [e for e in Kn.edges if e not in G.edges]
            for (u_i, u_j) in H.edges:
                for (v_r, v_s) in not_G_edges:
                    subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v1')
                    subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v2')
            subg.optimize()
            total_maps = 0
            all_maps = []
            while subg.SolCount > 0:
                mapping = get_restraints(G, H, subg.X)
                total_maps +=1
                pairs = []
                for i in range(m):
                    for j in range(n):
                        if mapping[i][j] == 1:
                            pairs.append((i, j))
                # print(pairs)
                all_maps.append(pairs)
                subg.addConstr(sum((X[i, j]) for (i, j) in pairs) <= m-1, name = 'Eliminating previous solution {total_maps}')
                subg.optimize()
    return all_maps         

def silent_subgraph_check(G, H):
    n = G.order()
    print(f'G has order {n}')
    j_n = np.ones(n)
    m = H.order()
    print(f'H has order {m}')
    j_m = np.ones(m)
    with gp.Env(empty = True) as env:
        env.setParam('OutputFlag', 0)
        env.start()
        with gp.Model('Subgraph', env=env) as subg:
            X = subg.addMVar((m, n), vtype = GRB.BINARY, name = 'map')
            subg.setObjective(sum(j_n[i] * j_m @ X[:, i] for i in range(n)), GRB.MINIMIZE)
            # each column should sum to at most 1
            for i in range(n):
                subg.addConstr(sum(X[:, i]) <= 1, name = f'Col {i} sum')
            # each row should sum to exactly 1    
            for i in range(m):
                subg.addConstr(sum(X[i, :]) == 1, name = f'Row {i} sum')
            # edge weight constraints
            Kn = nx.complete_graph(n)
            not_G_edges = [e for e in Kn.edges if e not in G.edges]
            for (u_i, u_j) in H.edges:
                for (v_r, v_s) in not_G_edges:
                    subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v1')
                    subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v2')
            # more edge weight constraints
            for (u_i, u_j) in H.edges:
                for (v_r, v_s) in G.edges:
                    if H[u_i][u_j]['color'] != G[v_r][v_s]['color']:
                        subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} color')
                        subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_s, v_r)} color')
            subg.optimize()
            total_maps = 0
            all_maps = []
            while subg.SolCount > 0:
                # print('Looking for another solution...')
                mapping = get_restraints(G, H, subg.X)
                total_maps +=1
                pairs = []
                for i in range(m):
                    for j in range(n):
                        if mapping[i][j] == 1:
                            pairs.append((i, j))
                # print(pairs)
                all_maps.append(pairs)
                subg.addConstr(sum((X[i, j]) for (i, j) in pairs) <= m-1, name = 'Eliminating previous solution {total_maps}')
                subg.optimize()
            print(f'Found {total_maps} solutions in all.')            
    return all_maps  
       
def edge_colored_graph(n, red_edges, blue_edges):
    G = nx.Graph()
    G.add_nodes_from(list(range(n)))
    G.add_edges_from(red_edges + blue_edges)
    for (u, v) in red_edges:
        G[u][v]['color'] = 'red'
    for (u, v) in blue_edges:
        G[u][v]['color'] = 'blue'
    return G

def print_board(graph, pos = None):
    if pos is None:
        pos = nx.circular_layout(graph)
    edge_colors = nx.get_edge_attributes(graph, 'color').values()
    nx.draw(graph, pos = pos, edge_color = edge_colors, node_color = 'grey', with_labels = True)
    plt.figure()

def count_solutions(maps_):
    images = []
    for m in maps_:
        image = []
        for v, v_prime in m:
            image.append(v_prime)
        check = True
        for i in images:
            if set(i) == set(image):
                check = False
        if check:
            images.append(image)
    num_solutions = len(images)
    print(f'There were {num_solutions} solutions found.')
    return num_solutions

def basic_subgraph_check(G, H):
    n = G.order()
    j_n = np.ones(n)
    m = H.order()
    j_m = np.ones(m)
    subg = gp.Model('Subgraph')
    X = subg.addMVar((m, n), vtype = GRB.BINARY, name = 'map')
    subg.setObjective(sum(j_n[i] * j_m @ X[:, i] for i in range(n)), GRB.MINIMIZE)
    # Column restraints
    for i in range(n):
        subg.addConstr(sum(X[:, i]) <= 1, name = f'Col{i} sum')
    # Row constraints
    for i in range(m):
        subg.addConstr(sum(X[i, :]) == 1, name = f'Row {i} sum')
    K_n = nx.complete_graph(n)
    not_G_edges = [e for e in K_n.edges if e not in G.edges]
    for (u_i, u_j) in list(H.edges):
        for (v_r, v_s) in not_G_edges:
            subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v1')
            subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v2')
    subg.optimize()
    
def basic_subgraph_check_result(G, H):
    n = G.order()
    j_n = np.ones(n)
    m = H.order()
    j_m = np.ones(m)
    with gp.Env(empty = True) as env:
        env.setParam('OutputFlag', 0)
        env.start()
        with gp.Model('Subgraph', env=env) as subg:
            X = subg.addMVar((m, n), vtype = GRB.BINARY, name = 'map')
            subg.setObjective(sum(j_n[i] * j_m @ X[:, i] for i in range(n)), GRB.MINIMIZE)
            # Column restraints
            for i in range(n):
                subg.addConstr(sum(X[:, i]) <= 1, name = f'Col{i} sum')
            # Row constraints
            for i in range(m):
                subg.addConstr(sum(X[i, :]) == 1, name = f'Row {i} sum')
            K_n = nx.complete_graph(n)
            not_G_edges = [e for e in K_n.edges if e not in G.edges]
            for (u_i, u_j) in list(H.edges):
                for (v_r, v_s) in not_G_edges:
                    subg.addConstr(X[u_i, v_r] + X[u_j, v_s] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v1')
                    subg.addConstr(X[u_i, v_s] + X[u_j, v_r] <= 1, name = f'Edges {(u_i, u_j)}, {(v_r, v_s)} v2')
            subg.optimize()
            if subg.SolCount == 0:
                return False
            else:
                return True
    
def graph_to_color(graph):
    n = graph.order()
    red = list(graph.edges)
    blue = [e for e in nx.complete_graph(n).edges if e not in red]
    graph = edge_colored_graph(n, red, blue)
    return graph