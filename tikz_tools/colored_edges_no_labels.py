import networkx as nx
from numpy import array
from nx_to_tikz import edge_colored_graph, nx_to_tikz_colored_edges

graph = nx.cycle_graph(5)
save_dir = 'C:/figures'
graph_name = 'color_no_label'
red_edges = [(0, 1), (1, 2)]
blue_edges = [(1, 2), (2, 3)]

# use a NetworkX layout,
#layout = nx.circular_layout(graph)
# or use a custom layout
layout = { # vertex: array([x_coord, y_coord]),
    0: array([0, 2]),
    1: array([1, -1]),
    2: array([-1.5, 1]),
    3: array([1.5, 1]),
    4: array([-1, -1])}

##########################################################################
##########################################################################
##########################################################################
############################# leave this alone :) ########################
##########################################################################
##########################################################################
##########################################################################

nx_to_tikz_colored_edges(edge_colored_graph(graph.order(), red_edges, blue_edges), layout, f'{save_dir}/{graph_name}')


