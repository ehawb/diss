import sys
import os
import tensorflow as tf
from multiprocessing import Process, Queue
from utils.observations import evaluate

""" How to use this module:
    if player is a trained model, indicate the name of the model as a
    string, and indicate how many MCTS rounds should be conducted and with
    what temperature.
    
    to observe play with a random agent, set the player name as 'random' and 
    you can just ignore the MCTS parameters.
    
    if you want to see the graph of every move printed, set print = 'all' 
        (they won't be printed until the end, and it might take a while!')
    if you want to see just the last graph printed, set print = 'end'
    to see no graphs printed, set print = None
    
    pause settings: 'games' or 'moves'
    
    interactive: True or False
    """

player1 = 'random'
p1_mcts_rounds = 1000
p1_mcts_temp = 0.0

player2 = 'random'
p2_mcts_rounds = 1000
p2_mcts_temp = 0.0


graph_order = 8
clique_orders = (3, 4)


num_workers = 6
games_per_worker = 2

#%% leave this part alone
if player1 != 'random':
    player1 = (f'models/{player1}', p1_mcts_rounds, p1_mcts_temp)
if player2 != 'random':
    player2 = (f'models/{player2}', p2_mcts_rounds, p2_mcts_temp)

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)    
encoder_name = '4_8_encoder'
print_settings = 'end'
pause_settings = 'never'
interactive = False

sys.path.append(os.getcwd())
num_games = games_per_worker
total_games = games_per_worker * num_workers
if __name__ == '__main__':
    num_p1_wins = 0
    total_moves = 0
    q = Queue()
    workers = []
    args = [q, player1, player2, graph_order, clique_orders, encoder_name,
        print_settings, pause_settings, interactive, num_games]
    for i in range(num_workers):
        worker = Process(target = evaluate, args = args)
        workers.append(worker)
        worker.start()
        print('Worker started.')
    
    for worker in workers:
        p1_wins, num_moves = q.get()
        num_p1_wins += p1_wins
        total_moves += num_moves
        worker.join()
    summary = f"""Player 1 wins out of {total_games}: {num_p1_wins}
    Average moves per game: {total_moves/total_games}"""
    