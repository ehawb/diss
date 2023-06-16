import networkx as nx
from numpy import array
from nx_to_tikz import nx_to_tikz_with_labels

graph = nx.cycle_graph(5)
save_dir = 'C:/figures'
graph_name = 'no_color_with_label'
label_dist = 0.1 # how far away the labels should be from vertices (takes trial and error sometimes...)

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

nx_to_tikz_with_labels(graph.edges, layout, f'{save_dir}/{graph_name}', label_dist)