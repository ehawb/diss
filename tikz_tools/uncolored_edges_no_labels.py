import networkx as nx
from numpy import array
from nx_to_tikz import nx_to_tikz, nx_to_tikz_with_labels

graph = nx.cycle_graph(5)

# use a NetworkX layout,
#layout = nx.circular_layout(graph)
# or use a custom layout
layout = { # vertex: array([x_coord, y_coord]),
    0: array([0, 1]),
    1: array([1, -1]),
    2: array([-1.5, 1]),
    3: array([1.5, 1]),
    4: array([-1, -1])}

nx_to_tikz(graph, layout)