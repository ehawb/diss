from tree_search_utils.tree_searcher import do_tree_search
import networkx as nx
import logging
from datetime import date

save_folder = 'E:/tree_search'

### put the graph6 specification inside the ''
#link_graph = nx.from_graph6_bytes(b'GsOiho') 
### or you can use a built in NetworkX class to build your graph
link_graph = nx.cycle_graph(5) 
### give your link graph a name 
link_graph_name = 'C_5'
### choose a tree search mode, 'BFS' or 'DFS'
search_mode = 'BFS'
### how many nodes of the tree do you want to explore before pickling?
pickle_freq = 1
### max number of children a node can have for the search
max_children = 1000 
### how large should constructions be allowed to get? 
### setting this ensures the search will halt eventually.
max_graph_order = 40 

################################################################################
################################################################################
####################### leave this stuff alone #################################
################################################################################
################################################################################
#%%
todays_date = date.today()
savefile = f'{link_graph_name}_tree_{date.today()}_max{max_graph_order}'
logging.basicConfig(filename=savefile,
filemode = 'a',
format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
datefmt='%H:%M:%S',
level=logging.DEBUG)

test, edges = do_tree_search(
        link_graph = link_graph,
        save_folder = save_folder,
        link_graph_name = link_graph_name,
        search_mode = search_mode,
        pickle_freq = pickle_freq,
        max_children = max_children,
        max_graph_order = max_graph_order
    )