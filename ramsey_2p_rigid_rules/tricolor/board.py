import networkx as nx
import copy
import itertools
from botparts.gametypes import Player

class Board:
    def __init__(self, graph):
        self.graph = graph
        self.edges = list(graph.edges)
        # color all edges black when Board is initialized:
        nx.set_edge_attributes(graph, 'black', name = 'color')
    
    def color_edge(self, edge, player):
        assert self.get_edge_color(edge) == ('black')
        u, v = edge
        self.graph[u][v]['color'] = player.color
    
    def get_edge_color(self, edge):
        u, v = edge # unpack the edge tuple
        edge_color = self.graph[u][v]['color']
        return edge_color

class Move():
    def __init__(self,
                 edge = None,
                 is_pass = False,
                 is_resign = False):
        if is_pass:
            print('passed.')
        if is_resign:
            print('resigned.')
        if edge is None:
            print('edge None.')
        assert (edge is not None) ^ is_pass ^ is_resign
        self.edge = edge
        self.is_play = (self.edge is not None)
        self.is_pass = is_pass
        self.is_resign = is_resign
    
    @classmethod
    def play(cls, edge):
        # if len(edge) == 3:
        #     edge = (edge[0], edge[1])
        return Move(edge = edge)
    
    @classmethod
    def pass_turn():
        return Move(is_pass = True)
    
    @classmethod
    def resign(cls):
        return Move(is_resign = True)
    
    def __str__(self):
        edge = self.edge
        return f'{edge}'
    
class GameState:
    """
    A class to represent a gamestate. The atrributes:
        board --> a Board object representing current graph
        player --> the player who will go next
        previous_state --> a GameState object representing previous state
        recent_move --> the previous move made to get to this gamestate
        clique_orders --> clique orders relevant to game
        red_subgraph, blue_subgraph, green_subgraph --> Graph objects
        red_cliques, blue_cliques, green_cliques --> lists of tuples representing vertices in cliques
        p1_edges, p2_edges --> list of tuples representing moves made by each player
    """
    def __init__(self, board, next_player, previous_state, recent_move,
                 clique_orders,
                 red_subgraph = nx.Graph(), red_cliques = [],
                 blue_subgraph = nx.Graph(), blue_cliques = [],
                 green_subgraph = nx.Graph(), green_cliques = [],
                 p1_edges = [], p2_edges = []):
        self.board = board
        self.player = next_player
        self.previous_state = previous_state
        self.last_move = recent_move
        self.colored_edge_list = self.get_colored_edge_list()
        self.red_subgraph = red_subgraph # subgraph induced by red edges
        self.red_cliques = red_cliques # a list of all red cliques (tuples) in the graph
        self.blue_subgraph = blue_subgraph # subgraph induced by blue edges
        self.blue_cliques = blue_cliques # a list of all blue cliques (tuples) in the graph
        self.green_subgraph = green_subgraph
        self.green_cliques = green_cliques
        if isinstance(clique_orders, int): # if one integer is passed through as clique size,
            self.red_clique_order = self.blue_clique_order = self.green_clique_order = clique_orders
        else:
            self.red_clique_order = clique_orders[0]
            self.blue_clique_order = clique_orders[1]
            self.green_clique_order = clique_orders[2]
        self.p1_edges = p1_edges
        self.p2_edges = p2_edges
            
    def get_colored_edge_list(self):
        edges = list(self.board.graph.edges)
        red_ind, blue_ind, green_ind, = (0,), (1,), (2,)
        red_edges = [edge + red_ind for edge in edges] # list of red edge representations
        blue_edges = [edge + blue_ind for edge in edges] # list of blue edge representations
        green_edges = [edge + green_ind for edge in edges] # list of green edge representations
        all_edges = red_edges + blue_edges + green_edges
        return all_edges
    
    def new_game(board, clique_orders):
        return GameState(board = board,
                         next_player = Player.p1, 
                         previous_state = None,
                         recent_move = None,
                         red_subgraph = nx.Graph(),
                         blue_subgraph = nx.Graph(),
                         green_subgraph = nx.Graph(),
                         red_cliques = [],
                         blue_cliques = [],
                         green_cliques = [],
                         clique_orders = clique_orders,
                         p1_edges = [],
                         p2_edges = [])
    
    def apply_move(self, move, update = True):
        color_dict = {0: 'red', 1: 'blue', 2: 'green'}
        if move.is_play:
            player = self.player
            # get the colored edge
            colored_edge = move.edge
            # this is the color indicator:
            color_ind = colored_edge[2]
            # get the appropriate color as a string
            color = color_dict[color_ind]
            # set the player's color accordingly
            player.set_color(color)
            # make a copy of the board to modify
            next_board = copy.deepcopy(self.board)
            # get the edge to be colored
            edge = (colored_edge[0], colored_edge[1])
            # color that edge with the appropriate color
            next_board.color_edge(edge, player)
            
        else:
            next_board = self.board
        p1_edges = self.p1_edges
        p2_edges = self.p2_edges
        if self.player == Player.p1:
            # update p1 edges
            p1_edges.append(colored_edge)
            # leave p2 edges alone
        else:
            # update p2 edges
            p2_edges.append(colored_edge)
        # need to update the subgraphs to reflect the previous move
        updated_gamestate = GameState(board = next_board,
                         next_player = self.player.other(),
                         previous_state = self,
                         recent_move = move,
                         clique_orders = (self.red_clique_order, self.blue_clique_order, self.green_clique_order),
                         red_subgraph = self.red_subgraph,
                         red_cliques = self.red_cliques,
                         blue_subgraph = self.blue_subgraph,
                         blue_cliques = self.blue_cliques,
                         green_subgraph = self.green_subgraph,
                         green_cliques = self.green_cliques,
                         p1_edges = p1_edges,
                         p2_edges = p2_edges)
        updated_gamestate = updated_gamestate.update_monochromatic_subgraph(color)
        cliques = updated_gamestate.check_monochromatic_cliques(move, color)
        if update == True:
            updated_gamestate = updated_gamestate.update_cliques(color, cliques)
        return updated_gamestate
    
    def is_over(self):
        """The game ends when a monochromatic clique of a certain order is formed."""
        recent_move = self.last_move
        edges_remaining = self.legal_moves()
        if len(edges_remaining) == 0:
            # print('no edges remaining.')
            return True
        if recent_move is None:
            return False
        if recent_move.is_resign:
            return True
        red_cliques = self.red_cliques
        winning_red_clique = self.red_clique_order
        blue_cliques = self.blue_cliques
        winning_blue_clique = self.blue_clique_order
        green_cliques = self.green_cliques
        winning_green_clique = self.green_clique_order
        all_cliques = red_cliques + blue_cliques + green_cliques
        if len(all_cliques) == 0:
            return False
        try:
            largest_red_clique = max(red_cliques, key = len)
        except ValueError:
            largest_red_clique = ()
        if len(largest_red_clique) >= winning_red_clique:
            # print(f'game over bc red clique: {largest_red_clique}')
            return True
        try:
            largest_blue_clique = max(blue_cliques, key = len)
        except ValueError:
            largest_blue_clique = ()
        if len(largest_blue_clique) >= winning_blue_clique:
            # print('game over bc blue clique')
            return True
        try:
            largest_green_clique = max(green_cliques, key = len)
        except ValueError:
            largest_green_clique = ()
        if len(largest_green_clique) >= winning_green_clique:
            # print('game over bc blue clique')
            return True
        else:
            colors = ['red', 'green', 'blue']
            for color in colors:
                self.update_monochromatic_subgraph(color)
            return False
        
    def update_monochromatic_subgraph(self, color):
        colored_edges = []
        graph = self.board.graph
        for (u, v, c) in graph.edges.data('color'):
            if c == color:
                colored_edges.append((u, v))
                # print(f'appending {color} {(u, v)}')
        subgraph = graph.edge_subgraph(colored_edges)
        # I want to figure out how to do this with a dictionary
        # if I get the time.
        if color == 'red':
            self.red_subgraph = subgraph
        elif color == 'blue':
            self.blue_subgraph = subgraph
        elif color == 'green':
            self.green_subgraph = subgraph
        return self
            
    def is_valid_move(self, move):
        if isinstance(move, tuple):
            if len(move) == 3:
                move = Move((move[0], move[1]))
            else:
                move = Move(move)
        if self.is_over():
            # print('not a valid move bc the game is over.')
            return False
        if move.is_pass or move.is_resign:
            return True
        if move.is_play:
            edge = move.edge
            u, v = move.edge
            if u > v:
                u1 = v
                v1 = u
                edge = (u1, v1)
            if edge not in self.board.edges:
                return False
            result = self.board.get_edge_color(edge)
            if result == 'black':
                return True
            else:
                return False
            
    def check_monochromatic_cliques(self, move, color):
        """Check if a particular move in a particular color results in a 
        monochromatic clique of the relevant size."""
        #### turn the move into something that can be worked with.
        if isinstance(move, tuple):
            edge = move
        else: 
            edge = move.edge
        edge = (edge[0], edge[1])
        u, v = edge
        # print(f'checking cliques after coloring {edge} {color}')
        ### get the info we need for relevant color
        if color == 'red':
            max_k = self.red_clique_order
            prior_cliques = self.red_cliques
            graph = self.red_subgraph
        elif color == 'blue':
            max_k = self.blue_clique_order
            prior_cliques = self.blue_cliques
            graph = self.blue_subgraph
        elif color == 'green':
            max_k = self.green_clique_order
            prior_cliques = self.green_cliques
            graph = self.green_subgraph        
        #### initialize list of actual cliques:
        cliques = []
        #### if there isn't a monochromatic subgraph,
        if graph is None:
            #### then there definitely aren't any cliques.
            return cliques
        # print(f'graph edges: {graph.edges()}')
        # print(f'(u, v): ({u}, {v})')
        #### if the edge colored isn't in the monochromatic subgraph,    ## why was I even worried about this? is it necessary?
        if (u, v) not in graph.edges():
            #### no cliques formed.
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
        for k in range(4, max_k+1):
            #### (remember that max_k is the order of the monochromatic clique
            #### we're trying to avoid in the original problem)
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
            #### get a list of vertex subsets that would complete a clique with this edge
            vertex_subsets = list(itertools.combinations(common_neighbors, k-2))
            #### if an edge doesn't exist between two common neighbors,
            #### we don't need to consider those neighbors, so first get a list
            #### of those dges
            common_neighbors_possible_edges = list(
                itertools.combinations(common_neighbors, 2))
            # print(f'common neighbors for {u} and {v}: {common_neighbors}')
            # print(f'possible edges: {common_neighbors_possible_edges}')
            #### now get a list of the edges that aren't actually there
            not_edges = [edge for edge in common_neighbors_possible_edges
                         if edge not in graph.edges()]
            # print(f'not edges: {not_edges}')
            for edge in not_edges:
                u1, v1 = edge
                vertex_subsets = [subset for subset in vertex_subsets if not 
                                  ((u1 in subset) and (v1 in subset))]
                #### remove trivial subsets
                vertex_subsets = [subset for subset in vertex_subsets if len(subset) > 1]
                # print(f'vertex subsets: {vertex_subsets}')
            #### now we can hunt for cliques
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
    
    def update_cliques(self, color, cliques):
        """Color should be a string representing the color of cliques to be updated.
        Cliques is a list of tuples that represent monochromatic cliques in the graph."""
        if len(cliques) == 0:
            return self
        # print(f'updating {color} cliques: {cliques}')
        board = self.board
        player = self.player
        previous_state = self.previous_state
        last_move = self.last_move
        clique_orders = (self.red_clique_order, self.blue_clique_order, self.green_clique_order)
        red_subgraph = self.red_subgraph
        red_cliques = self.red_cliques
        blue_cliques = self.blue_cliques
        blue_subgraph = self.blue_subgraph
        green_cliques = self.green_cliques
        green_subgraph = self.green_subgraph
        p1_edges = self.p1_edges
        p2_edges = self.p2_edges
        for clique in cliques:
            if color == 'red':
                red_cliques.append(clique)
                red_cliques = set(self.sort_cliques(red_cliques))
                red_cliques = list(red_cliques)
            elif color == 'blue':
                blue_cliques.append(clique)
                blue_cliques = set(self.sort_cliques(blue_cliques))
                blue_cliques = list(blue_cliques)
            elif color == 'green':
                green_cliques.append(clique)
                green_cliques = set(self.sort_cliques(green_cliques))
                green_cliques = list(green_cliques)
        gamestate = GameState(board = board,
                              next_player = player,
                              previous_state = previous_state,
                              recent_move = last_move,
                              clique_orders = clique_orders,
                              red_subgraph = red_subgraph,
                              red_cliques = red_cliques,
                              blue_subgraph = blue_subgraph,
                              blue_cliques = blue_cliques,
                              green_subgraph = green_subgraph,
                              green_cliques = green_cliques,
                              p1_edges = p1_edges,
                              p2_edges = p2_edges)
        return gamestate
    
    def sort_cliques(self, cliques):
        sorted_cliques = sorted(cliques, key = len)
        return sorted_cliques
        
    def legal_moves(self):
        candidates = []
        graph = self.board.graph
        for (u, v, c) in graph.edges.data('color'):
            if c == 'black':
                candidates.append((u, v))
        return candidates