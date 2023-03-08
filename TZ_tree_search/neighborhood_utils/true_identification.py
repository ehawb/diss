import networkx as nx

class SubgraphIdentification():
    
    def __init__(self, H, H_0, H_prime, H_0_prime, map_dict):
        self.base_dict = map_dict
        self.H = H
        self.H_0 = H_0
        self.H_prime = H_prime
        self.H_0_prime = H_0_prime
        self.H_prime_new = None
        self.union_graph = None
        
    def phi(self, node):
        for key, value in self.base_dict.items():
            if key == node:
                return value
        return None
    
    def phi_inverse(self, node):
        for key, value in self.base_dict.items():
            if value == node:
                return key
        return None
    
    def H_prime_relabeling(self):
        relabeling = {}
        max_node = max(self.H.nodes())
        next_node = max_node + 1
        for n in self.H_prime.nodes():
            if self.phi_inverse(n) is not None:
                # print(f'Node {n} was relabeled {self.phi_inverse(n)}')
                relabeling[n] = self.phi_inverse(n)
            else:
                # print(f'Node {n} needs to be relabeled as {next_node}.')
                relabeling[n] = next_node
                next_node += 1 
        return relabeling
    
    def relabel_H_prime(self):
        relabel = self.H_prime_relabeling()
        new = nx.relabel_nodes(self.H_prime, relabel)
        self.H_prime_new = new
        return new
    
    def H_0_prime_relabeling(self):
        relabeling = {}
        for n in self.H_0_prime.nodes():
            relabeling[n] = self.phi_inverse(n)
        return relabeling
    
    def relabel_H_0_prime(self):
        relabel = self.H_0_prime_relabeling()
        new = nx.relabel_nodes(self.H_prime, relabel)
        self.H_prime_relabeled = new
        return new
    
    def construct_union_graph(self):
        H_prime = self.relabel_H_prime()
        H_nodes = list(self.H.nodes())
        H_edges = list(self.H.edges())
        H_prime_nodes = list(H_prime.nodes())
        H_prime_edges = list(H_prime.edges())
        union = nx.Graph()
        all_nodes = list(set(H_nodes + H_prime_nodes))
        all_edges = list(set(H_edges + H_prime_edges))
        union.add_nodes_from(all_nodes)
        union.add_edges_from(all_edges)
        self.union_graph = union
        return union
    
    def get_link(self, vertex, graph):
        print(f'Getting link of node {vertex}')
        if vertex is None:
            print('Vertex has NoneType.')
            return nx.empty_graph()
        try:
            print('Gonna try to get some neighbors!')
            if vertex == 0:
                print(f'The neighbors are {list(nx.neighbors(graph, vertex))}')
            neighbors = list(nx.neighbors(graph, vertex))
        except:
            print(' Didnt get any neighbors...')
            return nx.empty_graph()
        return nx.subgraph(graph, neighbors)
    
    def is_true(self):


        def union_graph(G, H):
            union_nodes = list(set(list(G.nodes) + list(H.nodes)))
            union_edges = list(set(list(G.edges) + list(H.edges)))
            union = nx.Graph()
            union.add_nodes_from(union_nodes)
            union.add_edges_from(union_edges)
            return union
                   
        

        def check_H():
            print("----- Checking H -----")
            def condition_i(node, A_bar, B_bar):
                intersection = nx.intersection(A_bar, B_bar)
                # print(f"""     Condition i intersection info:
                #                   nodes {intersection.nodes}
                #                   edges {intersection.edges}
                      
                #       """)
                C = self.get_link(node, self.H_0)
                # print(f"""     Condition C intersection info:
                #                   nodes {C.nodes}
                #                   edges {C.edges}
                      
                #       """)
                if nx.is_isomorphic(intersection, C):
                    # check if all the edges are the same
                    if set(intersection.edges) == set(C.edges):
                        # print(f'Node {node} passed condition (i).')
                        return True
                return False

            def condition_ii(node, A_bar, B_bar):
                union = union_graph(A_bar, B_bar)
                # print(f'Graph 10 for node {node} has nodes {union.nodes} and edges {union.edges}')
                # print(f'     A_bar nodes: {A_bar.nodes}, edges: {A_bar.edges}')
                # print(f'     B_bar nodes: {B_bar.nodes}, edges: {B_bar.edges}')
                D = self.get_link(node, self.union_graph)
                if nx.is_isomorphic(union, D):
                    if set(union.edges) == set(D.edges):
                        # print(f'Node {node} passed condition (ii).')
                        return True
                return False
            
            for n in self.H.nodes():
                A = self.get_link(n, self.H)
                A_bar = A # this is how my code is set up...
                B = self.get_link(n, self.H_prime_new) # don't need to do phi(n) because of how I set it up.
                B_bar = B # also how my code is set up, I think...
                one, two = condition_i(n, A_bar, B_bar), condition_ii(n, A_bar, B_bar)
                if one and two:
                    continue
                else:
                    print(f'Failed on node {n}. (i) {one} (ii) {two}')
                    # continue
                    return False
            return True
        
        def check_H_prime():
            print("----- Checking H' -----")
            def condition_i(node, A_bar, B_bar):
                print(f'===== Condition (i) for {node} in H prime')
                intersection = nx.intersection(A_bar, B_bar)
                print(f'     Intersection has nodes {intersection.nodes} and edges {intersection.edges}')
                print(f' == Getting C ==')
                print(f'Node {node} has type {type(node)}')
                print(f'Some info about the H0_prime graph:')
                print(nx.info(self.H_0_prime))
                C = self.get_link(node, self.H_0_prime)
                print(f'   Before relabeling, C has nodes {C.nodes} and edges {C.edges}')
                C = nx.relabel_nodes(C, self.H_prime_relabeling())
                print(f'     C has nodes {C.nodes} and edges {C.edges}')
                if nx.is_isomorphic(intersection, C):
                    # check if all the edges are the same
                    if set(intersection.edges) == set(C.edges):
                        # print(f'Node {node} passed condition (i).')
                        return True
                return False

            def condition_ii(node, A_bar, B_bar):
                union = union_graph(A_bar, B_bar)
                # print(f"===== Condition (ii) for {node} in H_prime")
                # print(f"      The union graph has \n            nodes {union.nodes}  \n             edges {union.edges}")
                # print(f"Graph 10 in H' condition (ii) for node {node} has nodes {union.nodes} and edges {union.edges}")
                # print(f'     A_bar nodes: {A_bar.nodes}, edges: {A_bar.edges}')
                # print(f'     B_bar nodes: {B_bar.nodes}, edges: {B_bar.edges}')
                relabel = self.H_prime_relabeling()
                for key, item in relabel.items():
                    if key == node:
                        node_id = item
                        # print(f'Node {node} has been identified as {node_id}')
                D = self.get_link(node_id, self.union_graph)
                # print(f"     D has \n             nodes {D.nodes}  \n            edges {D.edges}")
                if nx.is_isomorphic(union, D):
                    if set(union.edges) == set(D.edges):
                        # print(f'Node {node} passed condition (ii).')
                        return True
                return False
                
        
            for n in self.H_prime.nodes():
                # print(f"===== Setting up for node {n} =======")
                relabel = self.H_prime_relabeling()
                A = self.get_link(n, self.H_prime)
                A_bar = nx.relabel_nodes(A, relabel)
                # print(f"     A bar: nodes {A_bar.nodes} \n           edges {A_bar.edges}")
                B = self.get_link(self.phi_inverse(n), self.H)
                B_bar = B # because H keeps all of its original labels
                # print(f"     B bar: nodes {B_bar.nodes} \n           edges {B_bar.edges}")
                one, two = condition_i(n, A_bar, B_bar), condition_ii(n, A_bar, B_bar)
                if one and two:
                    continue
                else:
                    print(f'Failed... on node {n}. (i) {one} (ii) {two}')
                    return False
                    # return False
            return True
        
        H_true = check_H()
        H_prime_true = check_H_prime()
        print(f"Results: \n H {H_true} \n H' {H_prime_true}")
        return True if H_true and H_prime_true else False      
        