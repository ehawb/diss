
# How to use the code
## The non-existence theorems
If you are interested in whether a graph might be ruled out as a potential link graph, you will want to use the `nonexist_thms.py` module on the main page. Just modify it to use the theorem you are interested in.
## Graph realization construction via tree search
- Use the `tree_search_setup.py` module on the main page. Comments are there to help you get it set up.
- If your computer stops in the middle of a search for some reason (or if you need to pause the search and resume it later), there is a `resume_tree_search.py` module.
- Once the tree search terminates, it will print where the data is saved. Copy this to paste in the next module:
- Open the `tree_search_results.py` module. Paste the path to the data.
- `realizers` will print information about the realizations found. A lot of that info is printed as a sort of sanity check. What's important is the graph6 code(s) given for realization(s).
- If you're curious about other graphs from the tree search, the `status` function takes data and a status as input. Potential statuses are outlined below:
    - `'TB'` (terminal, bad) will give information about graphs that ended up being bad for some reason -- probably an invalid subgraph somewhere.
    - `'TL'` (terminal, large) will give information about graphs that exceeded the maximum order of a realization allowed by the search.
- Just comment out `large` and `bad` if you don't care about them. :)
- If you're curious about what the actual search tree looks like, open the `draw_tree.py` module and paste the data path in. 
## Realization speedruns
- The `speedrun.py` module lets you run quick speed trials to find realizations of graphs.
- Load a list of graphs you'd like to run speed trials on. This can be a list of graph6 codes in some .txt file that NetworkX can read in as graph6 codes.
- Set an order limit on the realizations. The speed trials run on a depth-first search.
- Set a max number of children to explore from any particular node, if that's a concern.
- Finally, set the time limit (in seconds).
- During speed trials, the program looks for just *one* realization. If it finds one, it will move on to the next graph in the list.
- When the speed trials finish, go to the logging file. It contains info about results.
    - `[Y]` indicates a realization was found. In this case, it gives information about $L$ and $G$, where $G$ realizes $L$. It gives information about the time it took to find a realization and how many tree search nodes were explored in the process.
    - `[T]` indicates the program ran out of time.
    - `[N]` indicates that the tree search terminated for this particular $L$ and no realizations were found under the given constraints of time and realization order.
## A few more specifics about the code
### `neighborhood_utils`
Contains various modules related to the "neighborhood" (Trahtenbrot-Zykov) problem.
### `bhm` module
This module has an important function `thm_one`. It checks for realizability based on a theorem of Blass, Harary, and Miller. This theorem coincides with Theorem 13 in my dissertation. A proof of the theorem is available there.
### `bhm_gen` module
This module has an important function `thm_one_gen`. It checks for realizability based on a generalization of Blass, Harary, and Miller's theorem. This theorem coincides with Theorem 14 in my dissertation. A proof of the theorem is available there.
### `theorem_B` module
This module has two important functions:
`theorem_B_test` and `theorem_BC`
Both just take a potential link graph (NetworkX graph object) as input and return a result about whether the respective theorem of Hall rules it out as a link graph.
Theorem B is Theorem 15 in my dissertation. Theorem BC is Theorem 16 in my dissertation. Proofs of both theorems are available there. 
### `tree_search_utils`
All the bones for our realization construction program are here. I'm not sure it's important to know what all of the little pieces are, so I'm ok treating it as a sort of black box for now. Contact me if you have questions.


# Virtual environment
```
Package              Version
-------------------- -----------
anyio                3.6.1
argon2-cffi          21.3.0
argon2-cffi-bindings 21.2.0
asttokens            2.0.7
attrs                22.1.0
Babel                2.10.3
backcall             0.2.0
beautifulsoup4       4.11.1
bleach               5.0.1
certifi              2022.6.15
cffi                 1.15.1
charset-normalizer   2.1.0
colorama             0.4.5
cycler               0.11.0
debugpy              1.6.2
decorator            5.1.1
defusedxml           0.7.1
entrypoints          0.4
executing            0.9.1
fastjsonschema       2.16.1
fonttools            4.34.4
gurobipy             9.5.2
idna                 3.3
ipykernel            6.15.1
ipython              8.4.0
ipython-genutils     0.2.0
jedi                 0.18.1
Jinja2               3.1.2
json5                0.9.9
jsonschema           4.9.1
jupyter-client       7.3.4
jupyter-core         4.11.1
jupyter-server       1.18.1
jupyterlab           3.4.5
jupyterlab-pygments  0.2.2
jupyterlab-server    2.15.0
kiwisolver           1.4.4
lxml                 4.9.1
MarkupSafe           2.1.1
matplotlib           3.5.2
matplotlib-inline    0.1.3
mistune              0.8.4
nbclassic            0.4.3
nbclient             0.6.6
nbconvert            6.5.2
nbformat             5.4.0
nest-asyncio         1.5.5
networkx             2.8.5
notebook             6.4.12
notebook-shim        0.1.0
numpy                1.23.1
packaging            21.3
pandocfilters        1.5.0
parso                0.8.3
pickleshare          0.7.5
Pillow               9.2.0
pip                  22.2.2
prometheus-client    0.14.1
prompt-toolkit       3.0.30
psutil               5.9.1
pure-eval            0.2.2
pycparser            2.21
pydot                1.4.2
Pygments             2.12.0
pyparsing            3.0.9
pyrsistent           0.18.1
python-dateutil      2.8.2
pytz                 2022.1
pywin32              304
pywinpty             2.0.7
pyzmq                23.2.0
requests             2.28.1
scipy                1.9.0
Send2Trash           1.8.0
setuptools           63.2.0
six                  1.16.0
sklearn              0.0.post1
sniffio              1.2.0
soupsieve            2.3.2.post1
stack-data           0.3.0
terminado            0.15.0
tinycss2             1.1.1
tornado              6.2
traitlets            5.3.0
urllib3              1.26.11
wcwidth              0.2.5
webencodings         0.5.1
websocket-client     1.3.3
```
