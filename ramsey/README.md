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
This is a 2-player version of a Ramsey game. Two players alternate coloring the edges of a complete graph red and blue. The goal is to complete a red clique of order *s* or a blue clique of order *t*. The player does not have to claim all edges of the clique in order to win; they must simply complete a clique to win.

## Goals for this project

## Current work
Right now, everything is set up for playing an *R(3, 4)* game on a *K<sub>8</sub>*. This should become more general later, but for now, here's a brief description of milestones I'd like to meet before moving on to larger graphs:
- Achieve optimal play on *K<sub>8</sub>*, so end the game in a draw on a fairly consistent basis.
- See how this learning transfers to playing on a *K<sub>5</sub>* with the same model. Does the model need to see examples of playing the *K<sub>5</sub>* game first, or will it be able to apply what it learned in the *K<sub>8</sub>* game fairly well, basically treating the *K<sub>5</sub>* as a game within the *K<sub>8</sub>*?

## Some ideas for improvement
Instead of using the README to keep track of these, we can use the [issues tab](https://github.com/ehawb/ramsey_2p/issues). 

## How to use the bot
### Table of Contents
**[Setting up the virtual environment](#setting-up-the-virtual-environment)**<br>
**[Getting the bot on your computer](#getting-the-bot-on-your-computer)**<br>
**[Using the code](#using-the-code)**<br>

### Setting up the virtual environment
For Windows, entering the commands manually seems to be the most foolproof method. I've yet to get a spec list or .yml file to work for this (despite attempts on different machines). That said, run these commands in the Anaconda Powershell console:
```
conda create --name graphbot python=3.7
conda activate graphbot
conda install -n graphbot h5py=2.10.0
conda install -n graphbot keras=2.3.1
conda install -n graphbot networkx=2.4
conda install -n graphbot matplotlib=3.2.1
conda install -n graphbot spyder=4.1.5
pip install --upgrade tensorflow
conda install -n graphbot tensorflow-gpu=2.1.0
conda install -n graphbot scikit-learn
conda install -n graphbot dill
```

I've only really used Anaconda, so I don't know how this would work for anything else. I also use Spyder and don't know much about other IDEs. To run Spyder from the virtual environment, just activate the environment in the Anaconda Powershell and enter the command  ```spyder```.

### Getting the bot on your computer
First, I will describe how to clone the GitHub repository, and then I will talk about what that means.
Note: these instructions assume Git is already installed on your machine. Make sure you have Git installed if you don't already. Here is a [link to install Git](https://git-scm.com/downloads).
#### Cloning the repository
- Open Windows Command Prompt
- Change the directory to where you would like the bot to be stored on your computer (command: `cd/d <path>`)
  - In my example below, I decided I wanted to store the bot in a folder called "Test" (Note: This example screenshot shows a different game, but the process is the same.)
- Clone the GitHub repository into that folder using the following command: `git clone https://github.com/ehawb/pathgame.git`
- At this point, the bot is on your machine: 

![Screenshot of cloning process](https://github.com/ehawb/pathgame/blob/master/readme%20stuff%20(pics%20etc%2C%20irrelevant)/clone%20screenshot.png)

- Change the directory to the `ramsey_2p` module (command: `cd/d ramsey_2p`)
- You can see that Git is up and running by using command `git status`

#### Now what?
- You can create your own branch using the following command: `git checkout -b <branchname>`
  - In my example below, I decided to make a branch called `emily` (though more descriptive names might be preferable, e.g. "k20_bot".
  - Once you have your own branch, you can experiment with the code however you like without worrying about disrupting the stability of the `main` branch
  - You can create multiple branches if this is something you're interested in
  - To get back to the main branch (if you might want to make another new branch for an experiment), use the command `git checkout main`
  - If you do something you'd like to share, you can push your own branch to the GitHub by using the command `git push origin <branchname>`
  - Deleting branches, renaming branches, etc is fairly simple (commands are easily found on Google; there are also Git cheat sheets available)
  - If you'd like to keep track of any changes you've made in your branch, you can use Git commits to keep track of those changes (Colt Steele describes this stuff pretty well in [this video](https://www.youtube.com/watch?v=USjZcfj8yxE&list=PLmWO9U5bYOKLfrSv9QUAtVQHmEHEzymu9&ab_channel=ColtSteele))
- This is a good webpage about the GitHub workflow, which I'm still learning myself: [Understanding the GitHub flow](https://guides.github.com/introduction/flow/)
- This is a good webpage about pull requests on GitHub: [Creating a pull request](https://docs.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request) 
  ![Screenshot of branching process](https://github.com/ehawb/pathgame/blob/master/readme%20stuff%20(pics%20etc%2C%20irrelevant)/branch%2C%20push%20screenshot.png)
  
### Using the code
- The code as it is really isn't all that user friendly, so my apologies in advance...
- For the modules listed below, more details for each module will be given in the next section.
- To generate self play games, use the `self_play_configs` module.
- To train the bot on self play data, use the `z_train` module.
- To observe the bot playing some games, use the `bot_observations` module.

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
