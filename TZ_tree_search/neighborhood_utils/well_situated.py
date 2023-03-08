import networkx as nx

def well_situated(graph, subgraph):
    for u in subgraph.nodes:
        # print(f'Check node {u} in subgraph, all nodes are...')
        for v in [n for n in subgraph.nodes if n > u]:
            # print(f'Checking {u}, {v}')
            same_component = True
            try:
                nx.shortest_path(subgraph, u, v)
                # print(f'The shortest path from {u} to {v} has length {len(shortest_path)-1}')
            except:
                same_component = False
                continue
            if same_component:
                # print(f'{u} and {v} are in the same component.')
                shortest_path = nx.shortest_path(graph, u, v)
                if len(shortest_path)-1 <= 2:
                    print(f'{u} and {v} are close enough together to check.')
                    all_shortest_paths = list(nx.all_shortest_paths(graph, u, v))
                    print(f'All shortest paths from {u} to {v}: {list(all_shortest_paths)}')
                    for path in all_shortest_paths:
                        edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
                        print(f'The path {path} has edges {edges}')
                        for edge in edges:
                            if edge not in subgraph.edges():
                                return False
    return True