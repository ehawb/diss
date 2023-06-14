from tree_search_utils.tree_searcher import do_tree_check

def check_graphs(list_of_graphs, max_G_order, time_limit, max_children = 1000, redo = None):
    i = 1
    num_graphs = len(list_of_graphs)
    if redo is None:
        for link_graph in list_of_graphs:
            print(f'{i}/{num_graphs}...')
            n = link_graph.order()
            link_graph_name = f'order{n}_{i}'
            do_tree_check(link_graph = link_graph, link_graph_name = link_graph_name, search_mode = 'DFS', max_children = max_children, max_graph_order = max_G_order, time_limit = time_limit)
            i +=1
    else:
        for link_graph in list_of_graphs:
            print(f'{i}/{num_graphs}...')
            if i in redo:
                print(f'   redo.')
                n = link_graph.order()
                link_graph_name = f'order{n}_{i}'
                do_tree_check(link_graph = link_graph, link_graph_name = link_graph_name, search_mode = 'DFS', max_children = max_children, max_graph_order = max_G_order, time_limit = time_limit)
            i +=1
    return None