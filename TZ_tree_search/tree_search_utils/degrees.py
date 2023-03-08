def get_max_degree_node(graph, nodes):
    degrees = [(n, graph.degree(n)) for n in nodes]
    max_degree = 0
    max_node = None
    for n, degree in degrees:
        # print(f'      Node {n} has degree {degree}')
        if degree > max_degree:
            max_degree = degree
            # print(f'          Node {n} has the new max degree of {degree}')
            max_node = n
    # print(f'         Returning max node {max_node}')
    return max_degree

def get_min_degree_node(graph, nodes):
    degrees = [(n, graph.degree(n)) for n in nodes]
    min_degree = graph.order()
    min_node = None
    for n, degree in degrees:
        # print(f'      Node {n} has degree {degree}')
        if degree < min_degree:
            min_degree = degree
            # print(f'          Node {n} has the new max degree of {degree}')
            min_node = n
    # print(f'         Returning max node {max_node}')
    return min_degree