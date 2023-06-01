import networkx as nx
from neighborhood_utils.bhm import thm_one as thm_13
from neighborhood_utils.bhm_gen import thm_one_gen as thm_14
from neighborhood_utils.theorem_B import theorem_B_test as thm_15
from neighborhood_utils.theorem_B import theorem_BC as thm_16

### you just need a NetworkX graph object:
link_graph = nx.cycle_graph(5)
### you can also define it from a graph6 code, just put it in the '' below:
#link_graph = nx.from_graph6_bytes(b'GsOiho') 

### The following functions are available:
### thm_13(link_graph)
### thm_14(link_graph)
### thm_15(link_graph)
### thm_16(link_graph)
### I imported the names this way to match what's in my dissertation. 
### Just pass your link_graph through as input to the relevant function.
thm_16(test_graph)