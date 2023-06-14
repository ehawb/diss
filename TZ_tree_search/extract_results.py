import networkx as nx
from utils.gurobi_utils.gurobi_subgraphs import all_subgraph_check_plain
import pickle
import tempfile
import matplotlib.pyplot as plt
from utils.neighborhood_utils.neighborhood_counter import count_neighborhoods

data = 'E:/tree_search/08Oct2022_203009_ramsey34_1_BFS_FINAL.pickle'

def load_tree_data(data_path):
    with open(data_path, 'rb') as f:
        tree, edges = pickle.load(f)
    return tree, edges

def best_node(tree):
    best_edges = 0
    for node in tree:
        if node.status is not None:
            num_edges = len(node.local_graph.graph.edges)
            if num_edges > best_edges:
                best_edges = num_edges
                best_node = node
    return best_node

def good_finished_nodes(tree):
    good = []
    for node in tree:
        if node.status == 'TG':
            good.append(node)
    return good

def print_graph6(graph):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        nx.write_graph6(graph, f.name)
        _ = f.seek(0)
        str_ = str(f.read())
        g6 = str_.removeprefix("b'>>graph6<<")
        g6 = g6.removesuffix("\\n'")
        return g6

def present_good_graphs(data_path):
    tree, edges = load_tree_data(data_path)
    good_finish = good_finished_nodes(tree)
    print(f"=== There were {len(good_finish)} realizations found. === ")
    for f in good_finish:
        print(f"Info about the graph: {f}")
        print(f"Graph6 code: {print_graph6(f.local_graph.graph)}")
finishes = good_finished_nodes(tree)
for f in finishes:
    print(f"Info about the graph: {f}")
    print(f"Graph6 code: {print_graph6(f.local_graph.graph)}")
    