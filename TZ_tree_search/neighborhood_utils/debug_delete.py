from well_situated import well_situated
from true_identification import SubgraphIdentification
from annulus import Annulus
import matplotlib.pyplot as plt
import networkx as nx

# H = nx.cycle_graph(6)
# H_prime = nx.path_graph(6)

# check = well_situated(H, H_prime)
# print(check)

H = nx.cycle_graph(4)
H.add_edges_from([(0, 4), (3, 4), (1, 5), (2, 5)])
H_0 = nx.cycle_graph(4)

H_prime = nx.Graph([(0, 1), (1, 2), (2, 3), (0, 3),
                    (0, 4), (3, 5), (1, 6), (2, 7)])
H_00 = nx.cycle_graph(4)
nx.draw(H_prime, with_labels = True, pos = nx.circular_layout(H_prime))
plt.show()
mapping = {0:0, 1:1, 2:2, 3:3}

test_object = SubgraphIdentification(H, H_0, H_prime, H_00, mapping)
test_object.construct_union_graph()
# print(well_situated(H, H_0))
true_check = test_object.is_true()
# nx.draw(test_object.union_graph)
# plt.show()
# print(type(test_object.H_0_prime))
# print(nx.neighbors(test_object.H_0_prime, 0))