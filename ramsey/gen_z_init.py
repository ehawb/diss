import networkx as nx
import os
from botparts.board import Board
from botparts.encoders.k4_encoder_gen import K4Encoder
from models.resnet import dual_residual_network


graph_order = 8


graph = nx.complete_graph(graph_order)
board = Board(graph)
encoder = K4Encoder(graph_order)

num_edges = len(list(graph.edges()))

shape = encoder.shape()
model = dual_residual_network(num_edges, shape)

directory = f'models/K{graph_order}resnet_init'
os.mkdir(directory)
model.save(directory)