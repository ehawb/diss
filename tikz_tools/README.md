# How to use the code
This is code I used to generate some of the figures in my dissertation. This approach relies on taking a NetworkX graph object and a layout for it. A "layout" is just a Python dictionary that has coordinates for where each vertex should go. NetworkX has some built-in layouts (e.g. circular layout, spring embedding, etc), or you can provide your own layout for vertices.

You will need the following defined in the preamble of your document.
```
\tikzstyle{vertex}=[draw,circle,fill=black,text=white,inner sep=2pt]
\tikzstyle{vlab}=[shape=rectangle,fill=none,draw=none]
```

There are four modules to choose from:
- `uncolored_edges_no_labels` writes TikZ code for a graph with uncolored edges and unlabeled vertices
- `uncolored_edges_with_labels` writes TikZ code for a graph with uncolored edges and labeled vertices
- `colored_edges_no_labels` writes TikZ code for a graph with colored edges (right now, up to 2 colors, red and blue) and unlabeled vertices
- `colored_edges_with_labels` writes TikZ code for a graph with uncolored edges (right now, up to 2 colors, red and blue) and labeled vertices

# Virtual environment
```
Package    Version
---------- -------
networkx   2.8
numpy      1.24.3
pip        23.1.2
setuptools 65.5.0
```
