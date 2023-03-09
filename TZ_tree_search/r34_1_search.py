from tree_search_utils.tree_searcher import do_tree_search, resume_tree_search
import networkx as nx
import logging

#link_graph = nx.from_graph6_bytes(b'G@hZCc')
#link_graph_name = 'ramsey34_1'
link_graph = nx.cycle_graph(4)
link_graph_name = 'k3'
search_mode = 'BFS'
pickle_freq = 250
max_children = 1000
max_graph_order = 40

logging.basicConfig(filename='ramsey34_1tree',
filemode = 'a',
format = '%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
datefmt='%H:%M:%S',
level=logging.DEBUG)

data = 'E:/tree_search/24Sep2022_080719_ramsey34_1_BFS.pickle'
test, edges = do_tree_search(
    link_graph = link_graph,
    link_graph_name = link_graph_name,
    search_mode = search_mode,
    pickle_freq = pickle_freq,
    max_children = max_children,
    max_graph_order = max_graph_order
)

# resume_tree_search(
#     link_graph_name, 
#     data, 
#     search_mode, 
#     pickle_freq = pickle_freq, 
#     max_children = 1000, 
#     max_graph_order = max_graph_order, 
#     max_nodes = 1_000_000)