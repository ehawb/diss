import pickle
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt

def draw_actual_tree(search_nodes, edges, include_isomorphism = False, with_labels = False):
    tree = nx.Graph(edges)
    if not nx.is_tree(tree):
        print('Not a tree...')
        return 
    color_map = []
    status = ''
    for n in list(tree.nodes):
        for search_node in search_nodes:
            if search_node.ID == n:
                search_nodes.remove(search_node)
                status = search_node.status
        if status == 'IP':
            color_map.append('#8B9DA1') # brandeis ash
        elif status == 'TG':
            color_map.append('#98BD83') # parkway field laurel
        elif status == 'TB':
            color_map.append('#AD0000') # cardinal red
        elif status == 'CI':
            if include_isomorphism:
                color_map.append('#D9C982') # jefferson parchment
            else:
                tree.remove_node(n)
                tree.remove_edges_from([(u, v) for (u, v) in tree.edges if n in (u, v)])
        elif status == 'TL':
            if include_isomorphism:
                color_map.append('#7A6C53') # swain tobacco
            else:
                tree.remove_node(n)
                tree.remove_edges_from([(u, v) for (u, v) in tree.edges if n in (u, v)])
        elif status == 'D':
            color_map.append('#FFFFFF') # white
    node_size = 300 if with_labels else 200
    pos = graphviz_layout(tree, prog = "dot")
    nx.draw(tree, node_color = color_map, pos = pos,
    node_size = node_size, with_labels = with_labels,
    edgecolors = 'black')
    plt.show()

def load_tree_data(data_path):
    with open(data_path, 'rb') as f:
        tree, edges = pickle.load(f)
    return tree, edges

def draw_tree(data):
    tree, edges = load_tree_data(data)
    draw_actual_tree(tree, edges)