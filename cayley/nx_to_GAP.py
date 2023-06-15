import networkx as nx
from cayley_utils.nx_to_GAP import graph_to_GAP

# graph = nx.from_graph6_bytes('') 
graph = nx.cycle_graph(5)

### the code will save a GAP script. give a directory and a graph name here
save_dir = 'D:/gap_scripts'
graph_name = 'C5'

###############################################################################
###############################################################################
########################### leave this alone :) ################################
###############################################################################
###############################################################################
savefile = f'{save_dir}/{graph_name}'

graph_to_GAP(graph, savefile)