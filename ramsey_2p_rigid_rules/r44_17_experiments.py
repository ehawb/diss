from utils.observations import observe
import dill
import time 
""" How to use this module:
   see README on github 
    """
# init: 'r33_k5_init'
# V1: '2023_02_01_002_512'
# V2: '2023_02_02_002_512'

first_move_random = True

player1 ='r44_k17_init' 
p1_mcts_rounds = 250
p1_mcts_temp = 0.4

player2 = 'r44_k17_init' 
p2_mcts_rounds = 250
p2_mcts_temp = 0.4

headstart = None

encoder_name = 'k4_encoder'
graph_order = 17
clique_orders = (4, 4)
num_games = 1

print_settings = None
pause_settings = 'never'
interactive = False

#%% leave this part alone
start = time.time()
if player1 != 'random':
    player1 = (f'C:/users/emily/ramsey/ramsey_2p_rigid_rules/models/{player1}', p1_mcts_rounds, p1_mcts_temp)
if player2 != 'random':
    player2 = (f'C:/users/emily/ramsey/ramsey_2p_rigid_rules/models/{player2}', p2_mcts_rounds, p2_mcts_temp)
    

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