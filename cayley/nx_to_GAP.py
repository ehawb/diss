import networkx as nx 
import numpy as np

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
    print(adj_string)
    return adj_string

def graph_to_string_matrix(graph):
    adj_matrix = nx.to_numpy_matrix(graph)
    matrix_to_string(adj_matrix)

def graph_to_GAP(graph):
    graph_to_string_matrix(graph)
    n = graph.order()
    print(f"""graph :=  Graph( Group(()), [1..{n}], OnPoints, function(x,y) return A[x][y]=1; end, true );
    G := AutGroupGraph(graph);""")