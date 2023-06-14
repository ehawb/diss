def get_max_degree_node(graph, nodes):
    degrees = [(n, graph.degree(n)) for n in nodes]
    max_degree = 0
    max_node = None
    for n, degree in degrees:
        if degree > max_degree:
            max_degree = degree
            max_node = n
    return max_degree

def get_min_degree_node(graph, nodes):
    degrees = [(n, graph.degree(n)) for n in nodes]
    min_degree = graph.order()
    min_node = None
    for n, degree in degrees:
        if degree < min_degree:
            min_degree = degree
            min_node = n
    return min_degree