import sys
import os
import tensorflow as tf
from multiprocessing import Process, Queue
from utils.observations import evaluate

""" How to use this module:
See GitHub README
    """

model_save_dir = 'C:/users/emily/diss_repo/ramsey/models'

player1 = '2023_06_09_002_512'
p1_mcts_rounds = 1000
p1_mcts_temp = 0.0

player2 = '2023_06_09_002_512'
p2_mcts_rounds = 1000
p2_mcts_temp = 0.0

encoder_name = 'k3_encoder'
graph_order = 5
clique_orders = (3, 3)


num_workers = 4
games_per_worker = 2

#%% leave this part alone
if player1 != 'random':
    player1 = (f'{model_save_dir}/{player1}', p1_mcts_rounds, p1_mcts_temp)
if player2 != 'random':
    player2 = (f'{model_save_dir}/{player2}', p2_mcts_rounds, p2_mcts_temp)

gpus = tf.config.experimental.list_physical_devices('GPU')
tf.config.experimental.set_memory_growth(gpus[0], True)    
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
    