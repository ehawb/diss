import networkx as nx 

def matrix_to_string(adj_matrix):
    adj_string = 'A := ['
    num_rows, num_columns = adj_matrix.shape
    for i in range(num_rows):
        row = str(adj_matrix[i])
        row = row.replace("[[", "[")
        row = row.replace("]]", "]")
        row = row.replace(".]", "]")
        row = row.replace(". ", ",")
        row += ", \n"
        adj_string += row
    adj_string += "]"
    adj_string = adj_string.replace("], \n]", "]]")
    adj_string += ";"
    return adj_string

def graph_to_string_matrix(graph):
    adj_matrix = nx.to_numpy_matrix(graph)
    return matrix_to_string(adj_matrix)

def graph_to_GAP(graph, save = None):
    n = graph.order()
    matrix = graph_to_string_matrix(graph)
    gap_string = f"""{matrix} \n graph :=  Graph( Group(()), [1..{n}], OnPoints, function(x,y) return A[x][y]=1; end, true );
    G := AutGroupGraph(graph);"""
    if save is not None:
        with open(f'{save}.txt', 'w') as f:
            f.write(gap_string)
            f.close()
        print(f" ============= saved to {save}.txt ================== ")
    else:
        print(gap_string)