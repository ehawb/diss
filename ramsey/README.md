# ramsey_2p
2-player Ramsey game

## Table of Contents
**[Game description](#game-description)**<br>
**[Goals for this project](#goals-for-this-project)**<br>
**[Some ideas for improvement](#some-ideas-for-improvement)**<br>
**[How to use the bot](#how-to-use-the-bot)**<br>

## Game description
This is a 2-player version of the $r(k, l; n)$ game from my dissertation. 

## Goals for this project
It would be great if the bot could learn to play the $r(4, 4; 17)$ game well. My dissertation describes the challenges faced in that regard. The bot *did* learn to play the $r(3, 3; 5)$ game, and that data is included in my dissertation.

## Some ideas for improvement
My dissertation includes recommendations for continuing the project.

## How to use the bot
### Table of Contents
**[Setting up the virtual environment](#setting-up-the-virtual-environment)**<br>
**[Using the code](#using-the-code)**<br>
**[Workflow example](#workflow-example)**<br>

### Setting up the virtual environment
I have not had success using `.yml` files to work, so I just give a list of the commands I used to install the required packages here. Packages where I used specific versions will come with those version numbers; while updated versions of packages might do the job, I haven't yet experimented with that. These instructions are current as of June 2023.

The code requires Python version 3.7.9.

```
pip install keras==2.3.1
pip install networkx==2.4
pip install matplotlib
pip install --upgrade tensorflow
pip install tensorflow-gpu==2.1.0
pip install scikit-learn
pip install dill
```
  
### Using the code
- The code as it is really isn't all that user friendly, so my apologies in advance...
- For the modules listed below, more details for each module will be given in the next section.
- To generate self play games, use the `self_play_configs` module.
- To train the bot on self play data, use the `z_train` module.
- To observe the bot playing some games, use the `evaluate_progress` module.

#### Workflow example
Here is an example of how I used the code to train my agent to play the $r(3, 3; 5)$ game:
- Start with the `z_init` module. Define variables accordingly:
    - Set the `model_save_dir` to be where you want your models saved.
    - `graph_order = 5`
    - `cliques_order = (3, 3)`
    - `encoder_name = `k3_encoder`
- Run the module. When it finishes, your new model should be available where you saved it!
- Open the `self_play_configs` module. Define variables accordingly:
    - `model_save_dir` is the directory where your model is saved. You could copy and paste this from the `z_init` module.
    - `model_name` is the name of the model that should generate self-play games. This should be `initmodel_K5_3_3` from the previous step.
    - `experience_save_dir` is the directory where your model's experience should be saved.
     - `graph_order = 5`
    - `clique_orders = (3, 3)`
    - `encoder_name = `k3_encoder`
    - `MCTS_rounds` is up to you! How many rounds of MCTS should the agent carry out?
    - `MCTS_temp1` and `MCTS_temp2` are the temperatures for Player 1 and Player 2 respectively. I usually kept these the same, but sometimes I made them different just to see what happened.
    - `first_move_random` is True if you want Player1 to always select their first move randomly, false otherwise. This is helpful for getting more variety in the first move selection and helps avoid the same game being played over and over. 
    - `num_games` is the number of self-play games that should be played.
    - `num_workers` is the number of workers you want to carry out self play games in parallel. I used 4 workers for my hardware.
    - `games_per_batch` is how many games a worker should play before saving data. All of this will be combined at the end, but it was just a sanity thing for me in case I decided to end self play early or something.
- Run the module.
- Open the `z_train` module. Define variables accordingly:
    - `exp_location` is the directory where your experience is saved. This should be where the **combined** experience is saved.
         - For example, `C:/users/emily/diss_repo/ramsey/experience/01Jun2023_1648_2000games/combined` 
    - `model_save_dir` is the directory where your model is saved. You could copy and paste this from the `z_init` module.
    - `model_save_name` is the name of the model that completed self play. This should be `initmodel_K5_3_3` from the previous step.
    - `batch_size` is the number of samples that should be fed into the network at each step of training, i.e. the number of samples processed before weights are updated. I left it at 512 for all of my experiments, but feel free to change it.
    - `learning_rate` controls how much change in weights should be allowed at a time. If it's too large, you risk unstable training. If it's too small, you risk stagnant training. I usually left it at 0.002, but feel free to change it.
    - The other details (`graph_order`, `clique_order`, `encoder_name`, `MCTS_rounds`, and `MCTS_temp`) need to be set to initialize an agent for training. Just fill them in the same way you did in the `self_play_configs` step.
    - Run the module.
    - After training, it will print out details about where the model was saved.
 - Open the `evaluate_progress.py` module.
    - `model_save_dir` is same as before, where your model for evaluation is saved.
    - `encoder_name`, `graph_order`, and `clique_orders` are same as before.
    - `player1` should be the model for Player 1. At this step of the process, choose either the initialized model or the model you just trained.
    - Set the number of rollouts and the MCTS temperature Player 1 should have throughout the games.
    - Same for Player 2 -- choose a model to pit against Player 1 and set the other hyperparameters.
    - `first_move_random` should be set to `True` if the first move of each game should be random, `False` otherwise.
    - `num_games` is how many games to play for evaluation. I usually did 10 as an initial check, and if the results for those made me more curious, I'd do another trial of 100 games.
    - Run the module.
    - You can watch a play-by-play if you'd like, or just wait for all of the games to be over.
    - At the end, some statistics will be reported: How many games Player 1 lost, how many draws there were, the average number of moves across all games, and the amount of time elapsed.
 - Based on results from the progress evaluation, decide whether the original model (the one used in self play) needs more training, or if your newly trained model (produced by the `z_train` module) is ready to go to the self play phase.
 - Rinse and repeat...
