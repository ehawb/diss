from copy import deepcopy
import networkx as nx
import time
import logging
from gurobi_utils.gurobi_subgraphs import basic_subgraph_check_result as subgraph_check

available_IDs = list(range(1, 10_000_000))

def get_max_degree_node(graph, nodes):
    degrees = [(n, graph.degree(n)) for n in nodes]
    max_degree = 0
    max_node = nodes[0] # get a default return
    for n, degree in degrees:
        if degree > max_degree:
            max_degree = degree
            max_node = n
    return max_node

class Node():
    """Node for doing tree search on link problem.
    local_graph is a LocallyFGraph object
    children is a list of Node objects
    status can be one of the following:
    - 'TG' Terminal, good
    - 'IP' In progress
    - 'CI' Canceled, isomorphism
    - 'EC' Excessive children
    - 'TB' Terminal, bad
    - 'TL' Too large"""

    def __init__(self, local_graph, children = [], status = None, ID = 0):
        self.local_graph = local_graph
        self.children = children
        self.status = status
        self.ID = ID

    
    def __str__(self):
        node_desc = f"""
        ID: {self.ID}
        A node that has {len(self.children)} children and status {self.status}.
            The graph's order: {(self.local_graph.graph.order())}; 
            {len(self.local_graph.finished_nodes_)} finished vertices: {self.local_graph.finished_nodes_}.
        """
        return node_desc

    def update_status(self, finished_nodes):
        if self.status is None:
        # assume it's in progress...
            self.status = 'IP'
        else:
            if self.status == 'EC':
                return self.status
            if self.status == 'TL':
                return self.status
        if len(finished_nodes) == 0:
            return self.status
        for node in finished_nodes:
            if nx.is_isomorphic(node.local_graph.graph, self.local_graph.graph):
                self.status = 'CI'
                return self.status
        self.local_graph.finished_nodes()
        if self.local_graph.check_progress():
            if len(self.local_graph.unfinished_nodes()) == 0:
                print('Found a good finish.')
                self.status = 'TG'
        else:
            self.status = 'TB'
        
        for vertex in self.local_graph.graph.nodes:
            if not self.local_graph.check_neighborhood_status(vertex):
                self.status = 'TB'
        return self.status

    def set_status(self, status):
        self.status = status

    def expand(self, max_graph_order, max_children = 1000, resume = False, max_ID = None, time_limit = False):
        logging.debug('   Expanding...')
        if resume:
            global available_IDs
            remove_IDs = list(range(max_ID+1))
            # print(f'Need to remove IDs: {remove_IDs}')
            for i in remove_IDs:
                if i%500 == 0:
                    logging.info(f'Removing ID {i}...')
                try:
                    available_IDs.remove(i)
                except:
                    logging.info(f"{i} wasn't in the IDs. Moving on...")
        self.local_graph.finished_nodes()
        next_vertex = get_max_degree_node(self.local_graph.graph, self.local_graph.unfinished_nodes())
        add_children = []
        logging.debug('    Getting the children...')
        new_children = self.get_children(next_vertex, max_graph_order, max_children, time_limit)
        logging.debug(f'checking {len(new_children)} children')
        for i in range(len(new_children)):
            add = True
            next_graph = new_children[i]
            for j in range(i+1, len(new_children)):
                check_graph = new_children[j]
                if nx.is_isomorphic(check_graph.local_graph.graph, next_graph.local_graph.graph):
                    add = False
            if add:
                add_children.append(next_graph)
        self.children += add_children
        logging.debug('   Done expanding.')
        
    def reset_children(self):
        self.children = []

    def compare_node_lists(self, old, new):
        good = []
        i = 0
        for new_ in new:
            i +=1
            new_graph = True
            for old_ in old:
                if subgraph_check(old_.local_graph.graph, new_.local_graph.graph):
                    new_graph = False
                    continue
            if new_graph:
                good.append(new_)
        return good

    def get_children(self, node, max_graph_order, max_children = 1000, time_limit = False):
        if time_limit:
            start = time.time()
        children = []
        more_nodes_possible = self.local_graph.subgraph.order() - len(self.local_graph.get_neighbors(node))
        for add_nodes in range(more_nodes_possible + 1):
            if time_limit:
                time_remaining = time_limit - (time.time() - start)
                if time_remaining < 0:
                    return children
                logging.debug(f'   Getting nodes for adding {add_nodes} vertices; {time_remaining} seconds remaining.')
            self_copy = deepcopy(self)
            time_remaining = time_remaining if time_limit else time_limit
            possible_finishes = self_copy.local_graph.all_finishes(node, add_nodes, time_remaining)
            logging.debug(f'        Got {len(possible_finishes)} possible finishes')
            num_checked = 1
            for pf in possible_finishes:
                child_ID = available_IDs.pop(0)
                next_graph = deepcopy(self_copy.local_graph)
                next_graph.apply_finish(pf)
                if next_graph.graph.order() > max_graph_order:
                    next_node = Node(next_graph, children = [], status = 'TL', ID = child_ID)
                    children.append(next_node)
                    continue
                next_node = Node(next_graph, children = [], status = None, ID = child_ID)
                children.append(next_node)
                num_checked +=1 
                if len(children) > max_children:
                    return children
        return children

