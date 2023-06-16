import networkx as nx
from cayley_utils.nx_to_GAP import graph_to_GAP

### There are two ways to set up your graph. You can either enter the grpah6 code in the quotes below:
# graph = nx.from_graph6_bytes(b"") 
### Or you can use one of the graphs built in to the NetworkX library:
graph = nx.icosahedral_graph()

### the code will save a GAP script. give a directory and a graph name here
save_dir = 'D:/gap_scripts'
graph_name = 'icosahedron'

###############################################################################
###############################################################################
########################### leave this alone :) ################################
###############################################################################
###############################################################################
savefile = f'{save_dir}/{graph_name}'

graph_to_GAP(graph, savefile)