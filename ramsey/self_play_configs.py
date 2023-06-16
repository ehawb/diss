import os
import dill
import multiprocessing as mp
import time
import sys
import tensorflow as tf
from utils.self_play_main import parallel_self_play_games, combine_files

"""Note:

Instructions for how to use this module are on the GitHub README. Comments
seemed to really clutter up this code, which is why I chose to just write
the instructions there as opposed to including them here.    
    
"""
model_save_dir = 'C:/users/emily/diss_repo/ramsey/models'
model_name = 'initmodel_K5_3_3' 

experience_save_dir = 'C:/users/emily/diss_repo/ramsey/experience'

graph_order = 5
clique_orders = (3, 3)
encoder_name = 'k3_encoder'

MCTS_rounds = 100
MCTS_temp1 = 0.5
MCTS_temp2 = 0.5

first_move_random = True
num_games = 8
num_workers = 4
games_per_batch = 1

################################################################################
################################################################################
##################### leave this stuff alone :) ################################
################################################################################
################################################################################
#%% Leave this part alone:
MCTS_temps = [MCTS_temp1, MCTS_temp2]
#headstart can be a string that leads to the gamestate, or it can be None
headstart = None
trained_model = f'{model_save_dir}/{model_name}'
gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True) # multiprocessing GPU stuff
sys.path.append(os.getcwd()) # helps multiprocessing find all the modules

if headstart is None:
    head_start = None
else:
    with open(headstart, 'rb') as f:
        head_start = dill.load(f)
    f.close()

def main(num_games, num_workers, games_per_batch, exp_dir):
    full_exp_dir = f'{experience_save_dir}/{exp_dir}'
    os.mkdir(f'{full_exp_dir}')
    workers = []
    games_per_worker = num_games//num_workers
    num_batches = games_per_worker//games_per_batch
    for i in range(num_workers):
        worker_ID = i+1
        worker = mp.Process(target = parallel_self_play_games,
                            args = (trained_model, encoder_name, graph_order,
                                    clique_orders, MCTS_rounds, MCTS_temps,
                                num_batches, games_per_batch, full_exp_dir, worker_ID,
                                head_start, first_move_random))
        worker.start()
        workers.append(worker)
    for worker in workers:
        worker.join()
        
if __name__ == '__main__':
    start = time.time()
    date_time = time.strftime("%d%b%Y_%H%M")
    exp_dir = f'{date_time}_{num_games}games'
    main(num_games, num_workers, games_per_batch, exp_dir)
    combine_files(f'{experience_save_dir}/{exp_dir}')
    end = time.time()
    seconds = end - start
    minutes = seconds/60
    hours = minutes/60
    print(f'{num_games} games finished in {minutes} minutes; about {hours} hours.')