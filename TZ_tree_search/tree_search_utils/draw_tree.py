edges = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (1, 13), (1, 14), (1, 15), (1, 16), (1, 17), (1, 18), (1, 19), (1, 20), (1, 21), (1, 22), (13, 23), (13, 24), (13, 25), (13, 26), (13, 27), (13, 28), (13, 29), (13, 30), (13, 31), (13, 32), (23, 33), (23, 34), (23, 35), (23, 36), (23, 37), (23, 38), (23, 39), (33, 40), (33, 41), (33, 42), (40, 43), (40, 44), (40, 45), (40, 46), (43, 47), (43, 48), (43, 49), (43, 50), (43, 51), (47, 52), (47, 53), (52, 54), (52, 55), (44, 56), (44, 57), (46, 58), (46, 59), (46, 60), (42, 61), (42, 62), (42, 63), (42, 64), (35, 65), (35, 66), (35, 67), (35, 68), (35, 69), (35, 70), (35, 71), (35, 72), (36, 73), (36, 74), (36, 75), (36, 76), (36, 77), (36, 78), (75, 79), (27, 80), (27, 81), (27, 82), (27, 83), (27, 84), (27, 85), (27, 86), (27, 87), (27, 88)]

from numpy import array 
import networkx as nx
import pydot
from networkx.drawing.nx_pydot import graphviz_layout

def tree_levels(tree):
    levels = [[0]]
    layout = {}
    x, y = 0, 0
    vq = list(tree.nodes)
    finished = [0]
    while len(vq) > 0:
        previous_level = levels[-1]
        next_level = []
        for vertex in previous_level:
            next_level += [n for n in tree[vertex] if n not in finished]
        levels.append(next_level)
        finished += next_level
        vq = [n for n in vq if n not in finished]
        input(f'Next level: {next_level}')
        input(f'vertices left: {vq}')
    return levels

T = nx.Graph(edges)
pos = graphviz_layout(T, prog="twopi")
nx.draw(T, pos)
plt.show()