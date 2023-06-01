### Virtual environment
```
Package          Version
---------------- ----------
certifi          2022.12.7
distlib          0.3.6
filelock         3.9.0
gurobipy         10.0.1
networkx         3.0
pipenv           2022.12.19
platformdirs     2.6.2
virtualenv       20.17.1
virtualenv-clone 0.5.7
```
# How to use the code
First, I will explain what the code is.

## Modules
### `bhm` module
This module has an important function `thm_one`. It checks for realizability based on a theorem of Blass, Harary, and Miller. This theorem coincides with Theorem 13 in my dissertation. A proof of the theorem is available there.
### `bhm_gen` module
This module has an important function `thm_one_gen`. It checks for realizability based on a generalization of Blass, Harary, and Miller's theorem. This theorem coincides with Theorem 14 in my dissertation. A proof of the theorem is available there.
### `theorem_B` module
This module has two important functions:
`theorem_B_test` and `theorem_BC`
Both just take a potential link graph (NetworkX graph object) as input and return a result about whether the respective theorem of Hall rules it out as a link graph.
Theorem B is Theorem 15 in my dissertation. Theorem BC is Theorem 16 in my dissertation. Proofs of both theorems are available there. 

## How to use the modules
### The non-realizable theorems
If you are interested in whether a graph might be ruled out as a potential link graph, you will want to use the `nonexist_thms.py` module on the main page. Just modify it 
