from tree_search_utils.draw_tree import draw_tree
import os
os.environ["PATH"] += os.pathsep + 'C:/Program Files/Graphviz/bin/'

data = 'E:/tree_search/07Nov2022_084631_ramsey34_2_BFS.pickle' 
draw_tree(data)
