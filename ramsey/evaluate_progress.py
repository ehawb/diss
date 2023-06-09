from utils.observations import observe
import dill
import time 
""" How to use this module:
   see README on github 
    """

model_save_dir = 'C:/users/emily/diss_repo/ramsey/models'

player1 = '2023_06_09_002_512'
p1_mcts_rounds = 250
p1_mcts_temp = 0.4

player2 = '2023_06_09_002_512'
p2_mcts_rounds = 250
p2_mcts_temp = 0.4

first_move_random = True

encoder_name = 'k3_encoder'
graph_order = 5
clique_orders = (3, 3)
num_games = 10


################################################################################
################################################################################
##################### leave this stuff alone :) ################################
################################################################################
################################################################################
print_settings = None
pause_settings = 'never'
interactive = False
headstart = None
start = time.time()
if player1 != 'random':
    player1 = (f'{model_save_dir}/{player1}', p1_mcts_rounds, p1_mcts_temp)
if player2 != 'random':
    player2 = (f'{model_save_dir}/{player2}', p2_mcts_rounds, p2_mcts_temp)
    

if headstart is not None:
    with open(headstart, 'rb') as f:
        head_start = dill.load(f)
    f.close()
else:
    head_start = None
   
observe(player1, player2,
        graph_order, clique_orders, encoder_name,
        print_settings, pause_settings, interactive,
        num_games, head_start, first_move_random)

end = time.time()
print(f'{end-start} seconds elapsed.')