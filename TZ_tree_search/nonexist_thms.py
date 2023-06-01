import networkx as nx
from neighborhood_utils.bhm import thm_one as thm_13
from neighborhood_utils.bhm_gen import thm_one_gen as thm_14
from neighborhood_utils.theorem_B import theorem_B_test as thm_15
from neighborhood_utils.theorem_B import theorem_BC as thm_16

test_graph = nx.cycle_graph(5)
thm_16(test_graph)