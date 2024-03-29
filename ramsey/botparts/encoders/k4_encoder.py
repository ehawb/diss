import numpy as np
import itertools
from copy import deepcopy
from scipy.special import binom
from botparts.encoders.base import Encoder
from botparts.gametypes import Player

"""A summary of the planes in the K4 encoder:
    0 --> black edges
    1 --> Player red edges
    2 --> Player blue edges
    3 --> red edges
    4 --> blue edges
    5 --> red K3
    6 --> blue K3
    7 --> red K4
    8 --> blue K4

"""


class K4Encoder(Encoder):
    def __init__(self, graph_order):
        self.graph_order = graph_order
        self.num_planes = 7
        self.red_dict = {2: 1, 3: 3, 4: 5}
        self.blue_dict = {2: 2, 3: 4, 4: 6}
        self.main_dict = {'black': 0,
                          'red_k2': 1, 'blue_k2': 2,
                          'red_k3': 3, 'blue_k3': 4,
                          'red_k4': 5, 'blue_k4': 6,
                          }
       
    def name(self):
        return 'K4'
    
    def encode(self, game_state):
        # dictionaries containing axes where specific monochromatic cliques
        # of a particular order should be encoded
        red_dict = self.red_dict
        blue_dict = self.blue_dict
        board = deepcopy(game_state.board)
        graph = board.graph
        board_tensor = np.zeros(self.shape())
        red_edges = list(game_state.red_subgraph.edges)
        red_cliques = game_state.red_cliques
        red_cliques_edges = []
        for clique in red_cliques:
            edges = list(itertools.combinations(clique, 2))
            red_cliques_edges += edges
        for red_edge in red_edges:
            if red_edge not in red_cliques_edges:
                red_cliques.append(red_edge)
        blue_edges = list(game_state.blue_subgraph.edges)
        blue_cliques = game_state.blue_cliques
        blue_cliques_edges = []
        for clique in blue_cliques:
            edges = list(itertools.combinations(clique, 2))
            blue_cliques_edges += edges
        for blue_edge in blue_edges:
            if blue_edge not in blue_cliques_edges:
                blue_cliques.append(blue_edge)        
        for clique in red_cliques:
            clique_order = len(clique)
            clique_location = red_dict[clique_order]
            clique_edges = list(itertools.combinations(clique, 2))
            for edge in clique_edges:
                u, v = edge
                board_tensor[clique_location, u, v] = 1
                board_tensor[clique_location, v, u] = 1
        for clique in blue_cliques:
            clique_order = len(clique)
            clique_location = blue_dict[clique_order]
            clique_edges = list(itertools.combinations(clique, 2))
            for edge in clique_edges:
                u, v = edge
                board_tensor[clique_location, u, v] = 1
                board_tensor[clique_location, v, u] = 1
        # encoder should also include info about black (uncolored) edges:
        for (u, v, c) in graph.edges.data('color'):
             if c == 'black':
                 board_tensor[0, u, v] = 1
                 board_tensor[0, v, u] = 1
        return board_tensor
    
    def symmetric_encoding(self, game_state, shifted = None):
        if shifted is not None:
            board_tensor = shifted
        else:
            board_tensor = self.encode(game_state)
        black_tensor = board_tensor[0:1]
        player_tensor = np.concatenate([board_tensor[2:3], board_tensor[1:2]])
        k2_tensor = np.concatenate([board_tensor[4:5], board_tensor[3:4]])
        k3_tensor = np.concatenate([board_tensor[6:7], board_tensor[5:6]])
        k4_tensor = np.concatenate([board_tensor[8:], board_tensor[7:8]])
        symmetric_board_tensor = np.concatenate([black_tensor, player_tensor, k2_tensor, k3_tensor, k4_tensor])
        return symmetric_board_tensor
    
    def relabeled_encoding(self, game_state, shift):
        """Shift all the vertex labels by some constant in order to obtain
        a different encoding of the graph."""
        # dictionaries containing axes where specific monochromatic cliques
        # of a particular order should be encoded
        red_dict = self.red_dict
        blue_dict = self.blue_dict
        board = game_state.board
        graph = board.graph
        board_tensor = np.zeros(self.shape())
        current_color = game_state.player.color
        n = self.graph_order
        red_edges = list(game_state.red_subgraph.edges)
        red_cliques = game_state.red_cliques + red_edges
        blue_edges = list(game_state.blue_subgraph.edges)
        blue_cliques = game_state.blue_cliques + blue_edges
        red_shifted_edges = shift_edge_list(red_edges, shift, n)
        blue_shifted_edges = shift_edge_list(blue_edges, shift, n)
        red_shifted_cliques = shift_clique_list(red_cliques, shift, n)
        blue_shifted_cliques = shift_clique_list(blue_cliques, shift, n)
        for clique in red_shifted_cliques:
            clique_order = len(clique)
            clique_location = red_dict[clique_order]
            clique_edges = list(itertools.combinations(clique, 2))
            for edge in clique_edges:
                u, v = edge
                board_tensor[clique_location, u, v] = 1
                board_tensor[clique_location, v, u] = 1
        for clique in blue_shifted_cliques:
            clique_order = len(clique)
            clique_location = blue_dict[clique_order]
            clique_edges = list(itertools.combinations(clique, 2))
            for edge in clique_edges:
                u, v = edge
                board_tensor[clique_location, u, v] = 1
                board_tensor[clique_location, v, u] = 1
        # encoder should also include info about black (uncolored) edges:
        for (u, v, c) in graph.edges.data('color'):
             if c == 'black':
                 board_tensor[0, u, v] = 1
                 board_tensor[0, v, u] = 1
        # now deal with the player tensors
        player = game_state.player
        player_edges = game_state.p1_edges if player == Player.p1 else game_state.p2_edges
        player_dict = self.player_dict
        player_red = [edge for edge in player_edges if edge[2] == 0]
        player_blue = [edge for edge in player_edges if edge[2] == 1]
        player_red_shifted = shift_edge_list(player_red, shift, n)
        player_blue_shifted = shift_edge_list(player_blue, shift, n)
        p_red = player_dict['red']
        p_blue = player_dict['blue']
        for edge in player_red_shifted:
            u, v = edge
            board_tensor[p_red, u, v] = 1
            board_tensor[p_red, v, u] = 1
        for edge in player_blue_shifted:
            u, v = edge
            board_tensor[p_blue, u, v] = 1
            board_tensor[p_blue, v, u] = 1
        return board_tensor
    
    def encode_move(self, move, game_state):
        colored_edges = game_state.colored_edge_list
        color_ind = move[2]
        # if the edge is blue,
        if color_ind == 1:
            # only need to search latter half of edge list
            start = len(colored_edges)//2
        else:
            start = 0
        index = colored_edges.index(move, start)
        return index
    
    def decode_edge_index(self, index, game_state):
        colored_edges = game_state.colored_edge_list
        edge = colored_edges[index]
        return edge
    
    def num_points(self):
        n = self.graph_order
        k = 2
        num_moves = int(2 * binom(n, k)) # edges can be red or blue
        return num_moves
    
    def shape(self):
        return self.num_planes, self.graph_order, self.graph_order

def shift_clique_list(clique_list, shift, n):
    shifted_cliques = []
    for clique in clique_list:
        shifted_clique = tuple((x + shift)%n for x in clique)
        shifted_cliques.append(shifted_clique)
    return shifted_cliques
    
def shift_edge_list(edge_list, shift, n):
    """Takes a list of tuples and shifts all entries. Used for relabeling
    graphs."""
    shifted_edges = []
    for edge in edge_list:
        if len(edge) == 3:
            edge = (edge[0], edge[1])
        # get the shifted tuple
        shifted_edge = tuple((x + shift)%n for x in edge)
        # put it in the "right" order :) (not totally necessary but maybe nice
        # for debugging)
        u, v = shifted_edge
        if u > v:
            shifted_edge = (v, u)
        shifted_edges.append(shifted_edge)
    return shifted_edges        
        
def create(graph_order):
    return K4Encoder(graph_order)