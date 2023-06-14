import networkx as nx
import pickle
import tempfile

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

def finished_nodes_with_status(tree, status):
    nodes_with_status = []
    for node in tree:
        if node.status == status:
            nodes_with_status.append(node)
    return nodes_with_status

def print_graph6(graph):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        nx.write_graph6(graph, f.name)
        _ = f.seek(0)
        str_ = str(f.read())
        g6 = str_.removeprefix("b'>>graph6<<")
        g6 = g6.removesuffix("\\n'")
        return g6

def present_realizations(data_path):
    tree, edges = load_tree_data(data_path)
    good_finish = good_finished_nodes(tree)
    print(f"=== There were {len(good_finish)} realizations found. === ")
    for f in good_finish:
        print(f"Info about the graph: {f}")
        print(f"Graph6 code: {print_graph6(f.local_graph.graph)}")

def present_graphs_with_status(data_path, status):
    tree, edges = load_tree_data(data_path)
    status_finish = finished_nodes_with_status(tree, status)
    print(f"=== There were {len(status_finish)} graphs with status {status} found. === ")
    for f in status_finish:
        print(f"Info about the graph: {f}")
        print(f"Graph6 code: {print_graph6(f.local_graph.graph)}")