# dissertation_public
# About this repository
My name is Emily Hawboldt. This GitHub repository contains code to accompany my dissertation, "A machine learning approach to constructing Ramsey graphs leads to the Trahtenbrot-Zykov problem." I am a mathematician who occasionally uses programming to solve problems, so I ask folks to keep that in mind as they use my code. I make no guaranteees that the code presented here is completely polished and error-free, and I welcome feedback that more experienced programmers might like to share with me. 

## Chapter 3 stuff

## Chapter 4 stuff

## Chapter 5 stuff

My goal was to train a reinforcement learning agent to generate Ramsey counterexamples. While I succeeded on a small scale by generating the well-known R(3, 3) counterexample of order 5, my code did not scale well to working with larger graphs. If you are curious about the details of my project, I encourage you to read my dissertation.

## Setting up the virtual environment
I have not had success using `.yml` files to work, so I just give a list of the commands I used to install the required packages here. Packages where I used specific versions will come with those version numbers; while updated versions of packages might do the job, I haven't yet experimented with that. These instructions are current as of January 2023.

The code requires Python version 3.7.

```
pip install keras==2.3.1
pip install networkx==2.4
pip install matplotlib
pip install --upgrade tensorflow
pip install tensorflow-gpu==2.1.0
pip install scikit-learn
pip install dill
```
## How to use the code
