from asyncio import start_server
from utils.neighborhood_utils.locallyfgraphs import LocallyFGraph
from utils.tree_search_utils.tree_search import Node
from utils.gurobi_utils.gurobi_subgraphs import basic_subgraph_check_result as subgraph_check
import networkx as nx
import tempfile
from networkx.drawing.nx_pydot import graphviz_layout
import matplotlib.pyplot as plt
import time
import pickle
from copy import deepcopy
import logging

def do_pickle(graph_name, search_mode, data, final = False):
    date_time = time.strftime('%d%b%Y_%H%M%S')
    if final:
        savefile = f'E:/tree_search/{date_time}_{graph_name}_{search_mode}_FINAL.pickle'
    else:
        savefile = f'E:/tree_search/{date_time}_{graph_name}_{search_mode}.pickle'
    with open(savefile, 'wb') as handle:
        pickle.dump(data, handle)
        handle.close()
    if final:
        print(savefile)

def do_tree_search(link_graph, link_graph_name, search_mode, pickle_freq = 5, max_children = 1000, max_graph_order = 25, max_nodes = 1000000):
    start = time.time()
    tree_edges = []
    num_good = 0
    G = deepcopy(link_graph)
    starting_node = max(G.nodes) + 1
    G.add_edges_from([(n, starting_node) for n in G.nodes])
    queue = [Node(LocallyFGraph(G, link_graph))]
    finished_nodes = []
    i=0
    next_ID = 1
    while len(queue) > 0:
        if len(finished_nodes) == 0:
            pass
        elif len(finished_nodes)%pickle_freq == 0:
            print('Time to pickle!')
            do_pickle(graph_name = link_graph_name,
            search_mode = search_mode,
            data = (finished_nodes, tree_edges))
        print(f'===== Moving on in the queue {i}, {num_good} good finishes so far...........................')
        print(f'    Time elapsed: {time.time() - start}')
        next_node = queue.pop(0)
        print(f'       Next node: {next_node}')
        if next_node.status in ['TB', 'TL', 'CI', 'D']:
            finished_nodes.append(next_node)
            i+=1
            continue
        status = next_node.update_status(finished_nodes)
        print(f'Status: {status}')
        if status == 'TG':
            num_good +=1
        if status == 'IP':
            next_node.expand(max_graph_order)
            if len(next_node.children) > max_children:
                next_node = Node(next_node.local_graph, next_node.children[:max_children], 'EC')
            num_children = len(next_node.children)
            print(f'After expansion, need to add {num_children} children.')
            if search_mode == 'BFS':
                # new children at end of queue
                queue = queue + next_node.children
            elif search_mode == 'DFS':
                # push new children to top of queue
                queue = next_node.children + queue
            tree_edges += [(next_node.ID, child.ID) for child in next_node.children]
            next_ID += len(next_node.children)
            next_node.set_status('D')
        finished_nodes.append(next_node)
        print(f'{len(finished_nodes)} nodes finished so far.')
        if len(finished_nodes) > max_nodes:
            queue = []
        print(f'Queue length {len(queue)}')
        i +=1
    end = time.time()
    print(f'Took {end - start} seconds.')
    do_pickle(graph_name = link_graph_name, search_mode = search_mode, data = (finished_nodes, tree_edges), final = True)
    return finished_nodes, tree_edges

def get_max_ID(nodes):
    max_ID = 0
    for node in nodes:
        if node.ID > max_ID:
            max_ID = node.ID
    return max_ID

def resume_tree_search(link_graph_name, data, search_mode, pickle_freq = 5, max_children = 1000, max_graph_order = 25, max_nodes = 1_000_000):
    with open(data, 'rb') as f:
        nodes, tree_edges = pickle.load(f)
    start = time.time()
    num_good = 0
    queue = []
    for fnode in nodes:
        for child in fnode.children:
            if child.status is None:
                queue.append(child)
    finished_nodes = [node for node in nodes if node not in queue]
    print(f'Resuming tree search with {len(queue)} nodes in the queue and {len(finished_nodes)} nodes done.')
    i=0
    max_ID = get_max_ID(finished_nodes + queue)
    print(f'Max ID from previous search was {max_ID}')
    first_node = True
    while len(queue) > 0:
        if len(finished_nodes) == 0:
            pass
        elif len(finished_nodes)%pickle_freq == 0:
            print('Time to pickle!')
            do_pickle(graph_name = link_graph_name,
            search_mode = search_mode,
            data = (finished_nodes, tree_edges))
        print(f'===== Moving on in the queue {i}, {num_good} good finishes so far...........................')
        print(f'    Time elapsed: {time.time() - start}')
        next_node = queue.pop(0)
        print(f'       Next node: {next_node}')
        if next_node.status in ['TB', 'TL', 'CI', 'D']:
            finished_nodes.append(next_node)
            i+=1
            continue
        status = next_node.update_status(finished_nodes)
        print(f'Status: {status}')
        if status == 'TG':
            num_good +=1
        if status == 'IP':
            if first_node:
                next_node.expand(max_graph_order, resume = True, max_ID = max_ID)
                first_node = False
            else:
                next_node.expand(max_graph_order)
            if len(next_node.children) > max_children:
                next_node = Node(next_node.local_graph, next_node.children[:max_children], 'CT')
            num_children = len(next_node.children)
            # print(f'After expansion, need to add {num_children} children.')
            if search_mode == 'BFS':
                # new children at end of queue
                queue = queue + next_node.children
            elif search_mode == 'DFS':
                # push new children to top of queue
                queue = next_node.children + queue
            tree_edges += [(next_node.ID, child.ID) for child in next_node.children]
            next_node.set_status('D')
        finished_nodes.append(next_node)
        print(f'{len(finished_nodes)} nodes finished so far.')
        if len(finished_nodes) > max_nodes:
            queue = []
        print(f'Queue length {len(queue)}')
        i +=1
    end = time.time()
    print(f'Took {end - start} seconds.')
    do_pickle(graph_name = link_graph_name, search_mode = search_mode, data = (finished_nodes, tree_edges), final = True)
    return finished_nodes, tree_edges

def draw_tree(search_nodes, edges, include_isomorphism = False, with_labels = False):
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

def do_tree_check(link_graph, link_graph_name, search_mode, max_children = 1000, max_graph_order = 25, time_limit = 300):
    start = time.time()
    realizable = False
    tree_edges = []
    queue = []
    num_good = 0
    G = deepcopy(link_graph)
    logging.debug(f'----------- Looking at link graph {link_graph_name} with the info {nx.info(link_graph)} ========================== ')
    starting_node = max(G.nodes) + 1
    G.add_edges_from([(n, starting_node) for n in G.nodes])
    starter = Node(LocallyFGraph(G, link_graph))
    queue.append(starter)
    logging.debug(f'    starting with {len(queue)} nodes in the queue.')
    finished_nodes = []
    i=0
    next_ID = 1
    while len(queue) > 0:
        logging.debug(f'      Looking at another node. {len(queue)} nodes in the queue. {time.time() - start} seconds elapsed.')
        # print(f'===== Moving on in the queue {i}, {num_good} good finishes so far...........................')
        # print(f'    Time elapsed: {elapsed}')
        if time.time() - start > time_limit:
            logging.info(f'[T] {link_graph_name}  ({time_limit} s) | g6: {print_graph6(link_graph)} || explored {len(finished_nodes)} nodes')
            realizable = False
            return realizable
        next_node = queue.pop(0)
        logging.debug(f'          Node has {len(next_node.children)} children initially.')
        next_node.reset_children()
        logging.debug(f'          Node has {len(next_node.children)} children now.')
        # print(f'       Next node: {next_node}')
        if next_node.status in ['TB', 'TL', 'CI', 'D']:
            finished_nodes.append(next_node)
            i+=1
            continue
        status = next_node.update_status(finished_nodes)
        if status == 'TG':
            num_good +=1
            realizable = True
            logging.info(f'[Y] {link_graph_name}  g6 L: {print_graph6(link_graph)}   ||   g6 G: {print_graph6(next_node.local_graph.graph)}   ||  {int(time.time() - start)}s || explored {len(finished_nodes)} nodes')
            return realizable
        if status == 'IP':
            try:
                time_remaining = time_limit - (time.time() - start)
                next_node.expand(max_graph_order, time_limit = time_remaining)
            except:
                if len(next_node.local_graph.unfinished_nodes()) == 0:
                    logging.info(f'[Y] {link_graph_name} g6 L:  {print_graph6(link_graph)} | g6 G: {print_graph6(next_node.local_graph.graph)}  || unf 0 | {int(time.time() - start)}s || explored {len(finished_nodes)} nodes')
                    realizable = True
                    return realizable
            if len(next_node.children) > max_children:
                next_node = Node(next_node.local_graph, next_node.children[:max_children], 'EC')
            num_children = len(next_node.children)
            if search_mode == 'BFS':
                # new children at end of queue
                queue = queue + next_node.children
            elif search_mode == 'DFS':
                # push new children to top of queue
                logging.debug(f'   Adding {len(next_node.children)} nodes to the queue.')
                if len(next_node.children) > 0:
                    logging.debug(f"""     ABOUT THIS NODE: {next_node}
                                                FIRST CHILD: {next_node.children[0]}
                                                LINK GRAPH: {nx.info(next_node.local_graph.subgraph)}""")
                queue = next_node.children + queue
            next_ID += len(next_node.children)
            next_node.set_status('D')
        finished_nodes.append(next_node)
        i +=1
    if time.time() - start > time_limit:
        logging.info(f'[T] {link_graph_name}  ({time_limit} s) | g6: {print_graph6(link_graph)} || explored {len(finished_nodes)} nodes')
        realizable = False
        return realizable
    logging.info(f'[N] {link_graph_name} || g6 L: {print_graph6(link_graph)} || {int(time.time() - start)}s || explored {len(finished_nodes)} nodes')
    realizable = False
    return realizable

def print_graph6(graph):
    with tempfile.NamedTemporaryFile(delete=False) as f:
        nx.write_graph6(graph, f.name)
        _ = f.seek(0)
        str_ = str(f.read())
        g6 = str_.removeprefix("b'>>graph6<<")
        g6 = g6.removesuffix("\\n'")
        return g6    