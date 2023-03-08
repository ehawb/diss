from utils.observations import observe
import dill

""" How to use this module:
   see README on github 
    """

player1 = 'k8_four_blocks_init'
p1_mcts_rounds = 2500
p1_mcts_temp = 0.4

player2 = 'k8_four_blocks_init'
p2_mcts_rounds = 2500
p2_mcts_temp = 0.6

headstart = None

encoder_name = '4_8_encoder'
graph_order = 8
clique_orders = (3, 4)
num_games = 1

print_settings = None
pause_settings = 'never'
interactive = False

#%% leave this part alone
if player1 != 'random':
    player1 = (f'C:/users/emily/ramsey/ramsey_2p-main/models/{player1}', p1_mcts_rounds, p1_mcts_temp)
if player2 != 'random':
    player2 = (f'C:/users/emily/ramsey/ramsey_2p-main/models/{player2}', p2_mcts_rounds, p2_mcts_temp)
    

if headstart is not None:
    with open(headstart, 'rb') as f:
        head_start = dill.load(f)
    f.close()
else:
    head_start = None
   
observe(player1, player2,
        graph_order, clique_orders, encoder_name,
        print_settings, pause_settings, interactive,
        num_games, head_start)