from tree_search_utils.tree_searcher import do_tree_search, resume_tree_search
import networkx as nx
import logging
from datetime import date

### if resuming tree search, path to previous data goes here
# resume_data = 'C:/users/emily/dissertation/code/data/my_data'
# resume = True

### if not resuming previous search, indicate that here
resume = False
### put the graph6 specification inside the ''
#link_graph = nx.from_graph6_bytes(b'GsOiho') 
### or you can use a built in NetworkX class to build your graph
link_graph = nx.cycle_graph(5) 
### give your link graph a name 
link_graph_name = 'C_5'
### choose a tree search mode, 'BFS' or 'DFS'
search_mode = 'BFS'
### how many nodes of the tree do you want to explore before pickling?
pickle_freq = 250 
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

if not resume:
    test, edges = do_tree_search(
        link_graph = link_graph,
        link_graph_name = link_graph_name,
        search_mode = search_mode,
        pickle_freq = pickle_freq,
        max_children = max_children,
        max_graph_order = max_graph_order
    )

else:
    resume_tree_search(
        link_graph_name, 
        resume_data, 
        search_mode, 
        pickle_freq = pickle_freq, 
        max_children = 1000, 
        max_graph_order = max_graph_order, 
        max_nodes = 1_000_000)