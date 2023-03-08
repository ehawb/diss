import networkx as nx
import os
from botparts.board import Board
from botparts.encoders.base import Encoder
from models.four_blocks import fresh_model


graph_order = 17
cliques_order = (4, 4)
encoder_name = 'k4_encoder'

value_hidden_layer = 128
policy_hidden_layer = 128

#%% leave this part alone:
    
board = Board(nx.complete_graph(graph_order))
encoder = Encoder.get_encoder_by_name(encoder_name, graph_order)

model = fresh_model(encoder, value_hidden_layer, policy_hidden_layer)

if isinstance(cliques_order, int):
    cliques_order = (cliques_order, cliques_order)

directory = f'C:/users/emily/ramsey/ramsey_2p_rigid_rules/models/TEST_K{graph_order}_{cliques_order[0]}_{cliques_order[1]}'
os.mkdir(directory)
model.save(directory)