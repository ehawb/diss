import networkx as nx
from numpy import array
from nx_to_tikz import nx_to_tikz

graph = nx.cycle_graph(5)
save_dir = 'C:/users/emily smith/dissertation/figures/code_check'
graph_name = 'no_color_no_label'

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

nx_to_tikz(graph, layout, f'{save_dir}/{graph_name}')