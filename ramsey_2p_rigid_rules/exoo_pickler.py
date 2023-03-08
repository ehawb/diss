from utils.exoo_reader import pickle_2color_exoo

exoo_file = 'g4_8_58.txt'
graph_order = 58
clique_orders = (4, 8)

pickle_2color_exoo(exoo_file, clique_orders, graph_order)