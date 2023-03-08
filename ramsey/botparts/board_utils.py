"""Some board utilities:
    -a way to print a move made by a player
    -a way to print the current board
    -a way to get an edge move from user input"""

import networkx as nx
import matplotlib.pyplot as plt

def print_move(player, move):
    if move.is_pass:
        move_str = 'passes'
    if move.is_resign:
        move_str = 'resigns'
    else:
        move_str = f'{move.edge}'
    print(f'{player}: {move_str}')

def print_board(board):
    graph = board.graph
    plt.figure(dpi = 1200)
    pos = nx.circular_layout(graph)
    edge_colors = nx.get_edge_attributes(graph, 'color').values()
    nx.draw(graph, pos = pos, edge_color = edge_colors, node_color = 'grey',
            with_labels = True)
    plt.figure()
    
def edge_from_input(move):
    """Takes a move gotten from input and returns a tuple representing a move.
    This is necessary since all inputs are read as strings originally."""
    # first have to get rid of parentheses:
    move = move.replace('(', '')
    move = move.replace(')', '')
    # strip whitespace:
    move = move.strip()
    # get a list of vertices by splitting across comma:
    vertices = move.split(',')
    # convert them to integers:
    vertices = [int(vertex.strip()) for vertex in vertices]
    edge = tuple(vertices)
    print(f'edge: {edge}')
    return edge