import networkx as nx
import matplotlib.pyplot as plt
from true_identification import SubgraphIdentification

#%% Example 1
print('====================== Example 1 =========================')
H = nx.complete_graph(3)
H_subgraph = nx.Graph()
H_subgraph.add_nodes_from([0, 1, 2])
H_subgraph.add_edges_from([(0, 1)])

H_prime = nx.complete_graph(3)
H_prime.add_edges_from([(1, 3)])
H_prime_subgraph = nx.Graph()
H_prime_subgraph.add_nodes_from([0, 2, 3])
H_prime_subgraph.add_edges_from([(0, 2)])

mapping = {0:0, 1:2, 2:3}

test_object = SubgraphIdentification(H, H_subgraph, H_prime, H_prime_subgraph, mapping)
test_object.construct_union_graph()

true_check = test_object.is_true()
print(true_check)
#%% Example 2
print('====================== Example 2 =========================')
H = nx.complete_graph(3)
H_subgraph = nx.Graph()
H_subgraph.add_nodes_from([0, 1, 2])
H_subgraph.add_edges_from([(0, 1)])

H_prime = nx.complete_graph(3)
H_prime.add_edges_from([(1, 3)])
H_prime_subgraph = nx.Graph()
H_prime_subgraph.add_nodes_from([0, 1, 3])
H_prime_subgraph.add_edges_from([(0, 1)])

mapping = {0:0, 1:1, 2:3}

test_object = SubgraphIdentification(H, H_subgraph, H_prime, H_prime_subgraph, mapping)
test_object.construct_union_graph()

true_check = test_object.is_true()
print(true_check)
#%% Example 3
print('====================== Example 3 =========================')
H = nx.complete_graph(3)
H_subgraph = nx.Graph()
H_subgraph.add_nodes_from([0, 1, 2])
H_subgraph.add_edges_from([(0, 1), (1, 2)])

H_prime = nx.complete_graph(3)
H_prime.add_edges_from([(1, 3)])
H_prime_subgraph = nx.Graph()
H_prime_subgraph.add_nodes_from([1, 2, 3])
H_prime_subgraph.add_edges_from([(1, 2), (2, 3)])

mapping = {0:1, 1:2, 2:3}

test_object = SubgraphIdentification(H, H_subgraph, H_prime, H_prime_subgraph, mapping)
test_object.construct_union_graph()

true_check = test_object.is_true()
print(true_check)
#%% Example 4
print('====================== Example 4 =========================')
H = nx.Graph()
H.add_nodes_from(range(7))
H.add_edges_from([(0, 1), (0, 2), (0, 6), (1, 2), (1, 6),
                  (3, 4), (3, 5), (3, 6), (4, 5), (4, 6)])
H_subgraph = nx.Graph()
H_subgraph.add_nodes_from([0, 1, 2, 3, 4, 5])
H_subgraph.add_edges_from([(0, 1), (1, 2), (0, 2),
                           (3, 4), (3, 5), (4, 5)])

H_prime = nx.Graph()
H_prime.add_edges_from([(0, 6), (0, 10), (0, 3),
                        (1, 5), (1, 4), (1, 8),
                        (2, 4), (2, 6), (3, 7), (4, 6),
                        (7, 9), (8, 10), (8, 12), (9, 11), (10, 12)])
H_prime_subgraph = nx.Graph()
H_prime_subgraph.add_edges_from([(2, 4), (4, 6), (2, 6),
                                 (8, 10), (8, 12), (10, 12)])

mapping = {0:2, 1:4, 2:6, 3:8, 4:10, 5:12}

test_object = SubgraphIdentification(H, H_subgraph, H_prime, H_prime_subgraph, mapping)
test_object.construct_union_graph()

true_check = test_object.is_true()
print(true_check)