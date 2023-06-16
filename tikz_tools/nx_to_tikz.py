import networkx as nx
from itertools import combinations

def nx_to_tikz(graph, nx_layout, save_loc):
    if nx_layout is None:
        nx_layout = nx.circular_layout(graph)
    edges = list(graph.edges)
    v_string = ''
    for v in nx_layout:
        coords = nx_layout[v]
        x, y = coords[0], coords[1]
        v_string = v_string + f'{v}/{x}/{y},'
    # delete last comma
    v_string = v_string[:-1]
    edge_string = ''
    for edge in edges:
        u, v = edge
        edge_string = edge_string + f'{u}/{v},'
    # delete last comma
    edge_string = edge_string[:-1]
    code = f"""
        \\begin{{tikzpicture}}
            \\foreach \\v/\\x/\\y in {{{v_string}}}{{
                \\node[vertex] (a\\v) at (\\x, \\y) {{}};
                }}
            \\foreach \\u/\\v in {{{edge_string}}}{{
                \\draw (a\\u) -- (a\\v);
                }}
        \\end{{tikzpicture}}
        """
    with open(f'{save_loc}.tex', 'w') as f:
        f.write(code)
        f.close()
    print(f'Saved TikZ code to {save_loc}.tex')
    
def nx_to_tikz_with_labels(edges, nx_layout, save_loc, label_dist = 0.1):
    QI = ''
    QII = ''
    QIII = ''
    QIV = ''
    v_string = ''
    for v in nx_layout:
        coords = nx_layout[v]
        x, y = coords[0], coords[1]
        v_string = v_string + f'{v}/{x}/{y},'
        if x >= 0:
            if y >= 0:
                QI += f'{v}/{x}/{y},'
            else:
                QII += f'{v}/{x}/{y},'
        else:
            if y >= 0:
                QIV += f'{v}/{x}/{y},'
            else:
                QIII += f'{v}/{x}/{y},'
    edge_string = ''
    for edge in edges:
        u, v = edge
        edge_string = edge_string + f'{u}/{v},'
    # delete last comma
    v_string = v_string[:-1]
    QI = QI[:-1]
    QII = QII[:-1]
    QIII = QIII[:-1]
    QIV = QIV[:-1]
    # delete last comma
    edge_string = edge_string[:-1]
    code =f"""
        \\begin{{tikzpicture}}
            \\foreach \\v/\\x/\\y in {{{v_string}}}{{
                \\node[vertex] (a\\v) at (\\x, \\y) {{}};
                }}
            \\foreach \\v/\\x/\\y in {{{QI}}}{{
                \\node[vlab] () at (\\x+{label_dist}, \\y+{label_dist}){{\\v}};
                }}
            \\foreach \\v/\\x/\\y in {{{QII}}}{{
                \\node[vlab] () at (\\x+{label_dist}, \\y-{label_dist}){{\\v}};
                }}
            \\foreach \\v/\\x/\\y in {{{QIII}}}{{
                \\node[vlab] () at (\\x-{label_dist}, \\y-{label_dist}){{\\v}};
                }}
            \\foreach \\v/\\x/\\y in {{{QIV}}}{{
                \\node[vlab] () at (\\x-{label_dist}, \\y+{label_dist}){{\\v}};
                }}
            \\foreach \\u/\\v in {{{edge_string}}}{{
                \\draw (a\\u) -- (a\\v);
                }}
        \\end{{tikzpicture}}
        """
    with open(f'{save_loc}.tex', 'w') as f:
        f.write(code)
        f.close()
    print(f'Saved TikZ code to {save_loc}.tex')

def get_red_edges(graph):
    red = [(u, v) for (u, v) in graph.edges if graph[u][v]['color'] == 'red']
    return red

def get_blue_edges(graph):
    blue = [(u, v) for (u, v) in graph.edges if graph[u][v]['color'] == 'blue']
    return blue

def nx_to_tikz_colored_edges(graph, nx_layout, save_loc):
    red_edges = get_red_edges(graph)
    blue_edges = get_blue_edges(graph)

    v_string = ''
    for v in nx_layout:
        coords = nx_layout[v]
        x, y = coords[0], coords[1]
        v_string = v_string + f'{v}/{x}/{y},'
    # delete last comma
    v_string = v_string[:-1]
    red_string = ''
    for edge in red_edges:
        u, v = edge
        red_string = red_string + f'{u}/{v},'
    # delete last comma
    red_string = red_string[:-1]
    begin = "\\begin{tikzpicture}"
    vertex_code = f"""
            \\foreach \\v/\\x/\\y in {{{v_string}}}{{
                \\node[vertex] (a\\v) at (\\x, \\y) {{}};
                }}"""
    red_code = f"""
            \\foreach \\u/\\v in {{{red_string}}}{{
                \\draw[red] (a\\u) -- (a\\v);
                }}
        """
    blue_string = ''
    for edge in blue_edges:
        u, v = edge
        blue_string = blue_string + f'{u}/{v},'
    # delete last comma
    blue_string = blue_string[:-1]
    blue_code = f"""
            \\foreach \\u/\\v in {{{blue_string}}}{{
                \\draw[blue] (a\\u) -- (a\\v);
                }}
        """
    end = "\\end{tikzpicture}"
    code = f"""{begin}
    {vertex_code}
    {red_code}
    {blue_code}
    {end}
    """
    with open(f'{save_loc}.tex', 'w') as f:
        f.write(code)
        f.close()
    print(f'Saved TikZ code to {save_loc}.tex')

def nx_to_tikz_colored_edges_with_labels(graph, nx_layout, save_loc, label_dist = 0.01):
    red_edges = get_red_edges(graph)
    blue_edges = get_blue_edges(graph)
    black_edges = [e for e in graph.edges if e not in red_edges + blue_edges]
    QI = ''
    QII = ''
    QIII = ''
    QIV = ''
    v_string = ''
    for v in nx_layout:
        coords = nx_layout[v]
        x, y = coords[0], coords[1]
        v_string = v_string + f'{v}/{x}/{y},'
        if x >= 0:
            if y >= 0:
                QI += f'{v}/{x}/{y},'
                # input(f'vertex {v} in QI: {round(x, 5), round(y, 5)}')
            else:
                QII += f'{v}/{x}/{y},'
                # input(f'vertex {v} in QII {round(x, 5), round(y, 5)}')
        else:
            if y >= 0:
                QIV += f'{v}/{x}/{y},'
                # input(f'vertex {v} in QIII {round(x, 5), round(y, 5)}')
            else:
                QIII += f'{v}/{x}/{y},'
                # input(f'vertex {v} in QIV {round(x, 5), round(y, 5)}')
    # delete last comma
    v_string = v_string[:-1]
    QI = QI[:-1]
    QII = QII[:-1]
    QIII = QIII[:-1]
    QIV = QIV[:-1]
    red_string = ''
    for edge in red_edges:
        u, v = edge
        red_string = red_string + f'{u}/{v},'
    # delete last comma
    red_string = red_string[:-1]
    begin = "\\begin{tikzpicture}"
    vertex_code = f"""
            \\foreach \\v/\\x/\\y in {{{v_string}}}{{
                \\node[vertex] (a\\v) at (\\x, \\y) {{}};
                }}"""
    label_code = f"""
            \\foreach \\v/\\x/\\y in {{{QI}}}{{
                \\node[vlab] () at (\\x+{label_dist}, \\y+{label_dist}){{\\v}};
                }}
            \\foreach \\v/\\x/\\y in {{{QII}}}{{
                \\node[vlab] () at (\\x+{label_dist}, \\y-{label_dist}){{\\v}};
                }}
            \\foreach \\v/\\x/\\y in {{{QIII}}}{{
                \\node[vlab] () at (\\x-{label_dist}, \\y-{label_dist}){{\\v}};
                }}
            \\foreach \\v/\\x/\\y in {{{QIV}}}{{
                \\node[vlab] () at (\\x-{label_dist}, \\y+{label_dist}){{\\v}};
                }}"""
    red_code = f"""
            \\foreach \\u/\\v in {{{red_string}}}{{
                \\draw[red] (a\\u) -- (a\\v);
                }}
        """
    blue_string = ''
    for edge in blue_edges:
        u, v = edge
        blue_string = blue_string + f'{u}/{v},'
    # delete last comma
    blue_string = blue_string[:-1]
    blue_code = f"""
            \\foreach \\u/\\v in {{{blue_string}}}{{
                \\draw[blue] (a\\u) -- (a\\v);
                }}
        """
    black_string = ''
    for edge in black_edges:
        u, v = edge
        black_string = black_string + f'{u}/{v},'
    # delete last comma
    black_string = black_string[:-1]
    black_code = f"""
            \\foreach \\u/\\v in {{{black_string}}}{{
                \\draw[black] (a\\u) -- (a\\v);
                }}
        """
    end = "\\end{tikzpicture}"
    code = f"""{begin}
    {vertex_code}
    {label_code}
    {red_code}
    {blue_code}
    {black_code}
    {end}
    """
    with open(f'{save_loc}.tex', 'w') as f:
        f.write(code)
        f.close()
    print(f'Saved TikZ code to {save_loc}.tex')
    
def edge_colored_graph(n, red_edges, blue_edges, black_edges = []):
    G = nx.Graph()
    G.add_nodes_from(list(range(n)))
    G.add_edges_from(red_edges + blue_edges + black_edges)
    for (u, v) in red_edges:
        G[u][v]['color'] = 'red'
    for (u, v) in blue_edges:
        G[u][v]['color'] = 'blue'
    for (u, v) in black_edges:
        G[u][v]['color'] = 'black'
    return G