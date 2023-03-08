import networkx as nx
from itertools import combinations
from copy import deepcopy
from random import choice
import logging
import time
from utils.gurobi_utils.gurobi_subgraphs import basic_subgraph_check_result as subgraph_check
from utils.gurobi_utils.gurobi_subgraphs import all_subgraph_check_plain

def construct_locallyf_graph(F):
    G = nx.empty_graph(1)
    graph = LocallyFGraph(G, F)
    while len(graph.unfinished_nodes()) > 0:
        # print('===========================')
        graph.get_degrees()
        next_node = graph.unfinished_nodes()[0]
        # print(f'Finishing neighborhood of {next_node}...')
        graph.complete_neighborhood(next_node)
    return graph

def construct_locallyf_graph_quickstart(F):
    G = deepcopy(F)
    starting_node = max(G.nodes) + 1
    G.add_edges_from([(n, starting_node) for n in G.nodes])
    print(f'Starting graph info: {nx.info(G)}')
    graph = LocallyFGraph(G, F)
    while graph.possible_finish:
        try:
            next_node = graph.unfinished_nodes()[0]
        except IndexError:
            return graph
        print(f'Finishing neighborhood of {next_node}...')
        graph.complete_neighborhood(next_node)
    return graph

def construct_locallyf_graph_quickstart_random_order(F):
    G = deepcopy(F)
    starting_node = max(G.nodes) + 1
    G.add_edges_from([(n, starting_node) for n in G.nodes])
    print(f'Starting graph info: {nx.info(G)}')
    graph = LocallyFGraph(G, F)
    while graph.possible_finish:
        next_node = choice(graph.unfinished_nodes())
        print(f'Finishing neighborhood of {next_node}...')
        graph.complete_neighborhood(next_node)
    return graph

def construct_locallyf_graph_reverse_degree_order(F):
    G = deepcopy(F)
    starting_node = max(G.nodes) + 1
    G.add_edges_from([(n, starting_node) for n in G.nodes])
    graph = LocallyFGraph(G, F)
    while graph.possible_finish:
        print('===========================')
        graph.get_degrees()
        next_node = get_max_degree_node(graph.graph, graph.unfinished_nodes())
        if next_node is None:
            # print('Process finished.')
            return graph
        print(f'Finishing neighborhood of {next_node}...')
        graph.complete_neighborhood(next_node)
    return graph

def construct_locallyf_graph_degree_order(F):
    G = deepcopy(F)
    starting_node = max(G.nodes) + 1
    G.add_edges_from([(n, starting_node) for n in G.nodes])
    graph = LocallyFGraph(G, F)
    while graph.possible_finish:
        print('===========================')
        graph.get_degrees()
        next_node = get_min_degree_node(graph.graph, graph.unfinished_nodes())
        if next_node is None:
            # print('Process finished.')
            return graph
        print(f'Finishing neighborhood of {next_node}...')
        graph.complete_neighborhood(next_node, return_all=False)
    return graph

def get_max_degree_node(graph, nodes):
    degrees = [(n, graph.degree(n)) for n in nodes]
    max_degree = 0
    max_node = nodes[0] # get a default return
    for n, degree in degrees:
        # print(f'      Node {n} has degree {degree}')
        if degree > max_degree:
            max_degree = degree
            # print(f'          Node {n} has the new max degree of {degree}')
            max_node = n
    # print(f'         Returning max node {max_node}')
    return max_node

def get_min_degree_node(graph, nodes):
    degrees = [(n, graph.degree(n)) for n in nodes]
    min_degree = graph.order()
    min_node = nodes[0]
    for n, degree in degrees:
        # print(f'      Node {n} has degree {degree}')
        if degree < min_degree:
            min_degree = degree
            # print(f'          Node {n} has the new max degree of {degree}')
            min_node = n
    # print(f'         Returning max node {max_node}')
    return min_node

class LocallyFGraph():
    """ A class to represent a graph G which is locally H. """
    def __init__(self, graph, subgraph):
        self.graph = graph
        self.subgraph = subgraph
        self.finished_nodes_ = self.finished_nodes()
        self.possible_finish = True # later add conditions for if it's possible to finish the graph.

    def __str__(self):
        selfstring = f"""{nx.info(self.graph)}. Finished nodes: {self.finished_nodes()}"""
        return selfstring

    def get_neighbors(self, node):
        return list(self.graph.neighbors(node))
    
    def get_neighborhood_graph(self, node):
        neighbors = self.get_neighbors(node)
        return self.graph.subgraph(neighbors)
    
    def get_degrees(self):
        return [(n, self.graph.degree(n)) for n in self.graph.nodes]
            
    def check_neighborhood(self, node):
        neighborhood_graph = self.get_neighborhood_graph(node)
        result = nx.is_isomorphic(neighborhood_graph, self.subgraph)
        return result
    
    def add_edges(self, edges):
        self.graph.add_edges_from(edges)
    
    def add_nodes(self, nodes):
        self.graph.add_nodes_from(nodes)
        
    def finished_nodes(self):
        finished = []
        for n in self.graph.nodes:
            if self.graph.degree(n) == self.subgraph.order():
                if nx.is_isomorphic(self.get_neighborhood_graph(n), self.subgraph):
                    finished.append(n)
                    # print(f"Node {n} is finished.")
        self.finished_nodes_ = finished
        return finished
    
    def unfinished_nodes(self):
        return [n for n in self.graph.nodes if n not in self.finished_nodes_]
    
    def max_degree_nodes(self):
        maxed = []
        for n in self.graph.nodes:
            if self.graph.degree(n) == self.subgraph.order():
                maxed.append(n)
        return maxed
    
    def forbidden_edges(self, new_node = False):
        forbidden = []
        for n in self.finished_nodes():
            forbidden += [(v, n) for v in self.graph.nodes if v < n]
            forbidden += [(n, v) for v in self.graph.nodes if n < v]
            # can't add any more edges between neighbors of finished neighborhoods.
            forbidden += [(u, v) for (u, v) in combinations(self.get_neighbors(n), 2) if u !=v]
        # also can't add to any max degree nodes...
        for n in self.max_degree_nodes():
            forbidden += [(v, n) for v in self.graph.nodes if v < n]
            forbidden += [(n, v) for v in self.graph.nodes if n < v]
        forbidden = list(set(forbidden))
        return forbidden
    
    def check_progress(self):
        good = True
        finished_nodes = self.finished_nodes()
        for n in finished_nodes:
            if not nx.is_isomorphic(self.get_neighborhood_graph(n), self.subgraph):
                good = False
        degrees = self.get_degrees()
        for node, degree in degrees:
            # node degree is too large
            if degree > self.subgraph.order() + 1:
                good = False
        return good
    
    def get_allowed_edges(self, node):
        allowed = []
        forbidden_edges = self.forbidden_edges()
        for n in self.graph.nodes:
            if (node, n) not in forbidden_edges:
                if (n, node) not in forbidden_edges:
                    if n!= node:
                        if n < node:
                            allowed.append((n, node))
                        else:
                            allowed.append((node, n))
        return allowed
    
    def potential_neighborhood_finish(self, node):
        finished_nodes = self.finished_nodes()
        unfinished_nodes = [n for n in self.graph.nodes if n not in finished_nodes and n!=node]
        neighbors = self.get_neighbors(node)
        # maybe add edges among existing neighbors
        possible_ = list(combinations(neighbors + unfinished_nodes, 2))
        possible = []
        for (u, v) in possible_:
            if u <v:
                possible.append((u, v))
            elif v>u:
                possible.append((v, u))
        possible = [e for e in possible if e not in self.graph.edges]
        # if node == 3:
        #     print(f'neighbors: {neighbors}')
        #     print(f'possible edges: {possible}')
        # for unfinished nodes, maybe add edges there?
        for u in unfinished_nodes:
            if u < node:
                possible += [(u, node)]
            else:
                possible += [(node, u)]
        forbidden = self.forbidden_edges()
        bad_edges = []
        for (u, v) in possible:
            if u in finished_nodes:
                bad_edges.append((u, v))
            elif v in finished_nodes:
                bad_edges.append((u, v))
            elif (u, v) in forbidden:
                bad_edges.append((u, v))
            elif (v, u) in forbidden:
                bad_edges.append((u, v))
        good_edges = list(set([e for e in possible if e not in bad_edges]))
        return good_edges
    

    def complete_neighborhood(self, node, more_nodes = False, return_all = True):
        if more_nodes:
            if len(self.get_neighbors(node)) >= self.subgraph.order():
                self.possible_finish = False
                return []
            biggest_node = max(self.graph.nodes)
            self.add_edges([(node, biggest_node + 1)])
        edge_options = self.potential_neighborhood_finish(node)
        neighborhood_graph = self.get_neighborhood_graph(node)
        num_edges = len(neighborhood_graph.edges)
        sub_edges = len(self.subgraph.edges)
        num_edges_needed = sub_edges - num_edges
        if num_edges_needed == 0:
            return []
        possible_finishes = list(combinations(edge_options, num_edges_needed))
        good_finishes = []
        # print(f'Need to check {len(possible_finishes)} possible finishes...')
        i=1
        possible_finishes.reverse()
        for pf in possible_finishes:
            # if i %500 == 1:
                # print(f'--- checking {i} of {len(possible_finishes)}...')
            test_graph = deepcopy(self.graph)
            test_graph.add_edges_from(pf)
            test_graph = LocallyFGraph(test_graph, self.subgraph)
            if test_graph.check_progress():
                if nx.is_isomorphic(test_graph.get_neighborhood_graph(node), self.subgraph):
                    good_finishes.append(pf)
                    if not return_all:
                        self.apply_finish(pf)
                        return good_finishes
            i +=1
        if len(good_finishes) > 0:
            finish = good_finishes[0]
            self.apply_finish(finish)
            return good_finishes
        else:
            good_finishes += self.complete_neighborhood(node, more_nodes = True)
            return good_finishes

    def reduce_isomorphisms(self, node, list_of_finishes):
        unique_finishes = []
        finished_graphs = []
        num_checked = 1
        current_edges = self.graph.edges
        for f in list_of_finishes:
            # if num_checked%100 == 0:
                # print(f'{num_checked} isomorphisms checked...')
            num_checked +=1
            new = True
            G = nx.Graph(current_edges)
            G.add_edges_from(f)
            # G = deepcopy(self).apply_finish(f)
            for edge in f:
                u, v = edge
                check_u, check_v = None, None
                if u < node:
                    check_u = (u, node)
                elif u > node:
                    check_u = (node, u)
                if v < node:
                    check_v = (v, node)
                elif v > node:
                    check_v = (node, v)
                if check_u is None:
                    pass
                elif check_u not in G.edges:
                    G.add_edges_from([check_u])
                if check_v is None:
                    pass
                elif check_v not in G.edges:
                    G.add_edges_from([check_v])
            for H in finished_graphs:
                # print(f"G info: {nx.info(G)} \n H info: {nx.info(H)}")
                if nx.is_isomorphic(G, H):
                    # print("     Same graphs!")
                    new = False
                    break
            if new:
                # print(f"         Finish {i} was unique.")
                unique_finishes.append(f)
                finished_graphs.append(G)
        # print(f'Took a list of {len(list_of_finishes)} and reduced it down to {len(unique_finishes)}')
        return unique_finishes

    def all_finishes_old(self, vertex, more_nodes):
        # print(f'================= Finishes for expanding node {vertex} with {more_nodes} more nodes.')
        num_neighbors = len(self.get_neighbors(vertex))
        if num_neighbors + more_nodes < self.subgraph.order():
            if self.graph.order() + more_nodes < self.subgraph.order():
                # print('Gonna need more nodes than that.')
                return []
            # print('    Gonna need more nodes than that...')
            # return []
        while more_nodes > 0:
            biggest_node = max(self.graph.nodes)
            self.add_edges([(vertex, biggest_node + 1)])
            # print(f'    Added the vertex {biggest_node + 1}')
            more_nodes -= 1
        edge_options = self.potential_neighborhood_finish(vertex)
        neighborhood_graph = self.get_neighborhood_graph(vertex)
        num_edges = len(neighborhood_graph.edges)
        sub_edges = len(self.subgraph.edges)
        num_edges_needed = sub_edges - num_edges
        if num_edges_needed <= 0:
            return []
        possible_finishes = list(combinations(edge_options, num_edges_needed))
        # print(f'In all finishes, found {len(possible_finishes)} possible finishes.')
        # if len(possible_finishes) > 0:
            # possible_finishes = self.reduce_isomorphisms(vertex, possible_finishes)
        potential_finishes = []
        num_checked = 1
        current_edges = self.graph.edges
        for pf in possible_finishes:
            if num_checked%500 == 0:
                print(f'{num_checked}/{len(possible_finishes)} checked so far...')
            num_checked +=1
            new = True 
            # print(f'      Checking the possible finish {pf}')
            test_graph = nx.Graph(current_edges)
            # print(f'Test graph edges after deepcopy: {test_graph.edges}')
            test_graph.add_edges_from(pf)
            # print(f'Test graph edges after edges added from finish {pf}: \n {test_graph.edges}')
            for edge in pf:
                u, v = edge
                check_u, check_v = None, None
                if u < vertex:
                    check_u = (u, vertex)
                elif u > vertex:
                    check_u = (vertex, u)
                if check_u is None:
                    pass
                elif check_u not in test_graph.edges:
                    test_graph.add_edges_from([check_u])
                    # print(f"Finish before checking {check_u}: {pf}")
                    pf = pf + (check_u,)
                    # print(f"After: {pf}")
                if v < vertex:
                    check_v = (v, vertex)
                elif v > vertex:
                    check_v = (vertex, v)
                if check_v is None:
                    pass
                elif check_v not in test_graph.edges:
                    test_graph.add_edges_from([check_v])
                    pf = pf + (check_v,)
            # print(f"The graph after applying finish {pf} has edges \n {test_graph.edges}.")
            test_graph = LocallyFGraph(test_graph, self.subgraph)
            # print(f"The neighbors of vertex {vertex} in the graph are {test_graph.get_neighbors(vertex)}")
            if nx.is_isomorphic(test_graph.get_neighborhood_graph(vertex), self.subgraph):
                for gf in potential_finishes:
                    if sorted(gf) == sorted(pf):
                        print(f'        Found two equivalent finishes!')
                        new = False
                        break
                if new:
                    potential_finishes.append(pf)
        # print(f'        And now returning {len(potential_finishes)} potential finishes.')
        return potential_finishes
    
    def all_finishes(self, vertex, more_nodes, time_limit = False):
        if time_limit:
            start = time.time()
        forbidden = self.forbidden_edges()
        original_edges = self.graph.edges
        forbidden = [f for f in forbidden if f not in original_edges]
        # print(f'================= Finishes for expanding node {vertex} with {more_nodes} more nodes.')
        num_neighbors = len(self.get_neighbors(vertex))
        available_vertices = []
        available_vertices += self.unfinished_nodes()
        available_vertices = [v for v in available_vertices if v != vertex]
        available_vertices = [v for v in available_vertices if (v, vertex) not in forbidden]
        available_vertices = [v for v in available_vertices if (vertex, v) not in forbidden]
        neighborhood_graph = self.get_neighborhood_graph(vertex)
        already_neighbors = [v for v in neighborhood_graph.nodes]
        # print(f'Vertex {vertex} already has neighbors: {already_neighbors}')
        # print(f'Forbidden edges: {forbidden}')
        # print(f'Edges already there: {original_edges}')
        if num_neighbors + more_nodes < self.subgraph.order():
            if self.graph.order() + more_nodes < self.subgraph.order():
                # print('Gonna need more nodes than that.')
                return []
            # print('    Gonna need more nodes than that...')
            # return []
        while more_nodes > 0:
            biggest_node = max(self.graph.nodes)
            self.add_edges([(vertex, biggest_node + 1)])
            available_vertices.append(biggest_node+1)
            # print(f'    Added the vertex {biggest_node + 1}')
            more_nodes -= 1
        # print(f'The work continues...')
        # print(f'Available vertices: {available_vertices}')
        not_neighbors = [v for v in available_vertices if v not in already_neighbors]
        # print(f'Not neighbors: {not_neighbors}')
        num_vertices_needed = self.subgraph.order() - len(already_neighbors) 
        # print(f'Need {num_vertices_needed} more vertices.')
        if num_vertices_needed < 0:
            return []
        more_vertex_options = list(combinations(not_neighbors, num_vertices_needed))
        possible_finishes = []
        num_checked = 1
        current_edges = self.graph.edges
        # print(f'There are {len(more_vertex_options)} vertex options to explore...')
        for option in more_vertex_options:
            if time_limit:
                time_remaining = time_limit - (time.time() - start)
                logging.debug(f'Going through finishes with {time_remaining} seconds remaining.')
                if time_remaining < 0:
                    logging.debug(f'Ran out of time in all finishes.')
                    return good_finishes
            subgraph_vertices = already_neighbors + [u for u in option]
            # print(f'   Looking at subgraph with vertices {subgraph_vertices}')
            subgraph = self.graph.subgraph(subgraph_vertices) # maybe see if deepcopy is necessary
            # print(f'Got the subgraph.')
            node_assignments = {list(subgraph.nodes)[i]:list(range(self.subgraph.order()))[i] for i in range(subgraph.order())}
            # print(f'Node assignments: {node_assignments}')
            subgraph = nx.relabel_nodes(subgraph, node_assignments)
            # print('Got the graph relabeled.')
            embeddings = all_subgraph_check_plain(self.subgraph, subgraph)
            # print(f'Embeddings: {embeddings}')
            for embedding in embeddings:
                # print(f'Now looking at embedding {embedding}')
                dmap = {u:v for (u, v) in embedding}
                key_list = list(dmap.keys())
                val_list = list(dmap.values())
                nkeys = list(node_assignments.keys())
                nvals = list(node_assignments.values())
                new_edges = []
                explored_edges = []
                for edge in self.subgraph.edges:
                    # print(f' Checking da edge... {edge}')
                    u, v = edge
                    try:
                        u_pos, v_pos = val_list.index(u), val_list.index(v)
                    except ValueError:
                        summary = f"""The edge {edge} failed in value list. The dictionary map is {dmap} \n
                        The subgraph had edges {self.subgraph.edges} \n
                        The embedding was {embedding} \n
                        All of the embeddings are included below.... \n
                        {embeddings}
                        """
                        logging.debug(summary)
                        continue
                    pre_u, pre_v = key_list[u_pos], key_list[v_pos]
                    ou_pos, ov_pos = nvals.index(pre_u), nvals.index(pre_v)
                    ou, ov = nkeys[ou_pos], nkeys[ov_pos]
                    if ou < ov:
                        new_edge = (ou, ov)
                    else:
                        new_edge = (ov, ou)
                    explored_edges.append(new_edge)
                    # print(f'Preimage is {new_edge}')
                    if new_edge in original_edges:
                        # print(f'Edge {new_edge} isnt so new after all!')
                        continue
                    elif new_edge in forbidden:
                        # print(f'Embedding {embedding} introduced a bad edge: {new_edge}')
                        # print(f'Time to move on to next embedding.')
                        continue
                    else:
                        new_edges.append(new_edge)
                # print(f'Explored edges: {explored_edges}')
                # print(f'New edges: {new_edges}')
                # need to also add edges to any new neighbors
                # print(f'Adding the necessary edges to original vertex from option {option}')
                for v in option:
                    if v < vertex:
                        new_edge = (v, vertex)
                    else:
                        new_edge = (vertex, v)
                    # print(f'     edge is {new_edge}')
                    if new_edge in forbidden:
                        # print(f'Embedding {embedding} introduced forbidden edge {new_edge}')
                        # print('Gotta move on.')
                        continue
                    else:
                        new_edges.append(new_edge)
                # print('Time to sort those edges!')
                new_edges = sorted(list(set(new_edges)))
                # print(f'Current possible finishes: {possible_finishes}')
                # print(f'New edges {new_edges} in there? {new_edges in possible_finishes}')
                if new_edges not in possible_finishes:
                    # print('Got a new finish!')
                    possible_finishes.append(new_edges)
        good_finishes = []
        for pf in possible_finishes:
            # print(f'Need to check {len(possible_finishes)} finishes.')
            # if num_checked%500 == 0:
            #     print(f'{num_checked}/{len(possible_finishes)} checked so far...')
            num_checked +=1
            new = True 
            # print(f'      Checking the possible finish {pf}')
            test_graph = nx.Graph(current_edges)
            # print(f'Test graph edges after deepcopy: {test_graph.edges}')
            test_graph.add_edges_from(pf)
            # print(f'Test graph edges after edges added from finish {pf}: \n {test_graph.edges}')
            # for edge in pf:
            #     u, v = edge
            #     check_u, check_v = None, None
            #     if u < vertex:
            #         check_u = (u, vertex)
            #     elif u > vertex:
            #         check_u = (vertex, u)
            #     if check_u is None:
            #         pass
            #     elif check_u not in test_graph.edges:
            #         test_graph.add_edges_from([check_u])
            #         # print(f"Finish before checking {check_u}: {pf}")
            #         pf = pf + (check_u,)
            #         # print(f"After: {pf}")
            #     if v < vertex:
            #         check_v = (v, vertex)
            #     elif v > vertex:
            #         check_v = (vertex, v)
            #     if check_v is None:
            #         pass
            #     elif check_v not in test_graph.edges:
            #         test_graph.add_edges_from([check_v])
            #         pf = pf + (check_v,)
            # print(f"The graph after applying finish {pf} has edges \n {test_graph.edges}.")
            test_graph = LocallyFGraph(test_graph, self.subgraph)
            # print(f"The neighbors of vertex {vertex} in the graph are {test_graph.get_neighbors(vertex)}")
            if nx.is_isomorphic(test_graph.get_neighborhood_graph(vertex), self.subgraph):
                # for gf in potential_finishes:
                #     if sorted(gf) == sorted(pf):
                #         print(f'        Found two equivalent finishes!')
                #         new = False
                #         break
                # if new:
                good_finishes.append(pf)
        # print(f'        And now returning {len(potential_finishes)} potential finishes.')
        return good_finishes

    def apply_finish(self, finish):
        self.add_edges(finish)
        return self.graph
    
    def check_neighborhood_status(self, vertex):
        nbd_subgraph = self.get_neighborhood_graph(vertex)
        if nx.is_isomorphic(nbd_subgraph, self.subgraph):
            return True
        neighborhood = nx.convert_node_labels_to_integers(nbd_subgraph)
        if not subgraph_check(self.subgraph, neighborhood):
            return False
        if nbd_subgraph.order() == self.subgraph.order():
            # we can only work with the edges we've got.
            pf = [(u, v) for (u, v) in combinations(nbd_subgraph.nodes, 2) if u!=v]
            missing = [e for e in pf if e not in nbd_subgraph.edges]
            for e in missing:
                if e not in self.forbidden_edges():
                    return True
            # print('Unfinishable nbd...')
            return False
        return True
        