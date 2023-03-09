from tree_search_utils.tree_searcher import do_tree_check
import networkx as nx
import logging

logging.basicConfig(filename='E:/g7_10min_secondwave.log',
filemode = 'a',
format = '',
datefmt='',
level=logging.INFO)

mckay_graphs = nx.read_graph6('C:/users/emily/dissertation/code/data/mckay/graph7.g6')
graphs = mckay_graphs
order_limit = 30
time_limit = 600 
redo = [0, 1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 29, 31, 33, 35, 37, 38, 57, 58, 59, 60, 61, 62, 63, 64, 66, 68, 69,
        70, 71, 72, 73, 74, 76, 78, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 94, 96, 98, 103, 105, 112, 113, 120, 121, 122, 123, 124, 125, 128, 130, 132, 
        134, 136, 138, 144, 148, 149, 150, 151, 182, 183, 184, 185, 186, 187, 190, 193, 204, 205, 206, 208, 209, 211, 212, 216, 217, 221, 224, 228, 240, 242, 243, 264,
          267, 324, 346, 347, 349, 354, 355, 356, 359, 362, 369, 370, 371, 372, 373, 374, 375, 377, 379, 381, 382, 384, 386, 388, 389, 390, 391, 393, 394, 397, 403, 406,
            411, 412, 413, 422, 452, 453, 462, 470, 485, 488, 491, 501, 502, 505, 509, 511, 528, 532, 553, 554, 556, 558, 561, 566, 568, 569, 571, 572, 573, 582, 584, 587,
              593, 594, 596, 597, 598, 601, 604, 605, 607, 611, 620, 643, 644, 646, 699, 774, 785, 795, 847, 849, 915, 916, 921, 923, 925, 993]

def check_graphs(list_of_graphs, max_G_order, time_limit, redo = None):
    i = 0
    num_graphs = len(list_of_graphs)
    if redo is None:
        for link_graph in list_of_graphs:
            print(f'{i}/{num_graphs}...')
            n = link_graph.order()
            link_graph_name = f'order{n}_{i}'
            do_tree_check(link_graph = link_graph, link_graph_name = link_graph_name, search_mode = 'DFS', max_children = 1000, max_graph_order = max_G_order, time_limit = time_limit)
            i +=1
    else:
        for link_graph in list_of_graphs:
            print(f'{i}/{num_graphs}...')
            if i in redo:
                print(f'   redo.')
                n = link_graph.order()
                link_graph_name = f'order{n}_{i}'
                do_tree_check(link_graph = link_graph, link_graph_name = link_graph_name, search_mode = 'DFS', max_children = 1000, max_graph_order = max_G_order, time_limit = time_limit)
            i +=1
        # if i == 5:
        #     return None
    return None

check_graphs(graphs, order_limit, time_limit, redo = redo)