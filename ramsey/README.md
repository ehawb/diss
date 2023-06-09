# ramsey_2p
2-player Ramsey game

## Table of Contents
**[Game description](#game-description)**<br>
**[Goals for this project](#goals-for-this-project)**<br>
**[Current work](#current-work)**<br>
**[Some ideas for improvement](#some-ideas-for-improvement)**<br>
**[How to use the bot](#how-to-use-the-bot)**<br>
**[Descriptions of some key modules](#descriptions-of-some-key-modules)**<br>

## Game description
This is a 2-player version of the $r(k, l; n)$ game from my dissertation. 

## Goals for this project
It would be great if the bot could learn to play the $r(4, 4; 17)$ game well. My dissertation describes the challenges faced in that regard. The bot *did* learn to play the $r(3, 3; 5)$ game, and that data is included in my dissertation.

## Some ideas for improvement
My dissertation includes recommendations for continuing the project.

## How to use the bot
### Table of Contents
**[Setting up the virtual environment](#setting-up-the-virtual-environment)**<br>
**[Getting the bot on your computer](#getting-the-bot-on-your-computer)**<br>
**[Using the code](#using-the-code)**<br>

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


## Descriptions of some key modules
### Self play generator (`self_play_configs`)
#### Instructions for use
- The `trained_model` should be a string, something like `my_model`.
- `graph_order` should be an integer; should also stay consistent for the time being (e.g. always playing on graph of order 8).
- `clique_orders` can be an integer or a tuple; if an integer *k* is entered, this is equivalent to entering the tuple *(k, k)*.
- Designate the MCTS rounds and temperature for the self play bot. Note: You might want to observe different temperatures in the `observations` module to choose a good temperature to use for self play. This parameter usually is set by trial and error.
- Designate the number of workers to use in multiprocessing
- Designate the total number of games to play, shared across all workers
#### Some other notes
- Games will be saved in batches of 10; this is so data is saved often, which makes it less of a big deal if something weird happens (e.g. power outage) or if self play is ended early for some reason
- If self play does terminate early (whether by choice or not), the data can easily be consolidated using the `combine_files` module
### Bot training (`z_train`)
- `exp_location` should be the full path of where experience data is stored. I implemented it this way to allow data from external drives to be easily used if necessary. To get this quickly, just go to the folder where experience is saved, right click the address, and copy it. This will paste into Spyder as a string. 
- `model_location` should be something like `my_model`, just the model ID.
- The rest of the variables are pretty self explanatory.

### Bot observations (`observations_configs`)
#### Instructions for use
- If a trained model should be used for a player, indicate the name of the model as a string.
- If one of the players should be a random bot, enter `'random'` as the player name.
- If a player is random, the MCTS parameters can be set to 0 or just be simply ignored (they won't be used).
```python
player1 = '04_13_model_A'
p1_mcts_rounds = 1000
p1_mcts_temp = 0.03

player2 = 'random'
p2_mcts_rounds = 0
p2_mcts_temp = 0
```
- `graph_order` and `clique_orders` are similar as before; integer for `graph_order`, integer or tuple for `clique_orders`
- `num_games` is the number of games you'd like to observe between the bots.
- `print_settings` There are three different choices for what to enter here.
  - `print_settings = None` don't print any of the graphs created by the bots
  - `print_settings = 'end'` print the graph created at the end of the game
  - `print_settings = 'all'` print the graph created after each move. Note: they won't all be printed until the game is over (just how matplotlib works), and depending on the number of edges colored, this could take a while. But it's an option!
- `pause_settings` There are three different choices for what to enter here.
  -  `pause_settings = None` no pauses are taken; just run the games back-to-back
  -  `pause_settings = 'games'` pause after each game
  -  `pause_settings = 'moves'` pause after each move
- `interactive` There are two different choices for what to enter here.
  - `interactive = True` use the "interactive" version of the bot that lets you watch the tree search unfold (works best for a smaller number of MCTS rounds if you're curious about what's going on within the tree search)
  - `interactive = False` use the regular version of the bot. Some information about the tree search is still reported (visit counts for each node) but fewer details are seen.


