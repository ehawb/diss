# How to use the code
This is code I used to generate some of the figures in my dissertation. This approach relies on taking a NetworkX graph object and a layout for it. A "layout" is just a Python dictionary that has coordinates for where each vertex should go. NetworkX has some built-in layouts (e.g. circular layout, spring embedding, etc), or you can provide your own layout for vertices.

You will need the following defined in the preamble of your document.
```
\tikzstyle{vertex}=[draw,circle,fill=black,text=white,inner sep=2pt]
\tikzstyle{vlab}=[shape=rectangle,fill=none,draw=none]
```
## TikZ code for graphs with uncolored edges

## TikZ code for graphs with colored edges

# Virtual environment
```
Package    Version
---------- -------
networkx   2.8
numpy      1.24.3
pip        23.1.2
setuptools 65.5.0
```
