import networkx as nx
import os
from botparts.board import Board
from botparts.encoders.base import Encoder
from models.four_blocks import fresh_model

model_save_dir = 'C:/users/emily/diss_repo/ramsey/models'

graph_order = 5
cliques_order = (3, 3)
encoder_name = 'k3_encoder'

value_hidden_layer = 128
policy_hidden_layer = 128

################################################################################
################################################################################
##################### leave this stuff alone :) ################################
################################################################################
################################################################################
    
board = Board(nx.complete_graph(graph_order))
encoder = Encoder.get_encoder_by_name(encoder_name, graph_order)

model = fresh_model(encoder, value_hidden_layer, policy_hidden_layer)

if isinstance(cliques_order, int):
    cliques_order = (cliques_order, cliques_order)

directory = f'{model_save_dir}/initmodel_K{graph_order}_{cliques_order[0]}_{cliques_order[1]}'
os.mkdir(directory)
model.save(directory)