from tensorflow.keras.models import load_model
import networkx as nx
import os
import numpy as np
from copy import deepcopy
from botparts.encoders.base import Encoder
from botparts.encoders.experience import ZeroExperienceCollector
from botparts.encoders.experience import combine_experience, save_experience
from botparts.gametypes import Player
from botparts.zero.agent_main import ZeroAgent
from botparts.board import GameState, Board
from utils.simulations import end_game_eval, game_info


def game_sim(board, clique_orders, player1, collector1, player2, collector2, head_start = None, first_move_random = False):
    collector1.begin_episode()
    player1.set_collector(collector1)
    collector2.begin_episode()
    player2.set_collector(collector2)
    if head_start is None:
        game = GameState.new_game(board, clique_orders)
    else:
        head_start.player = Player.p1
        game = deepcopy(head_start)
        
    print('------------------------ beginning the game. ------------------------ ')
    i=1
    agents = {Player.p1: player1, Player.p2 : player2}
    first_node = agents[game.player].create_node(game)
    node = deepcopy(first_node)
    while not game.is_over():
        print(f'current player: {game.player} type: {type(game.player)}')
        if i == 1:
            if first_move_random:
                move, node = agents[game.player].select_move(node, random = True)
        move, node = agents[game.player].select_move(node)
        game = game.apply_move(move)
        print(f'move {i}: {move} ')
        i +=1
    print('game over! info:')
    game_info(game)
    agents[game.player].collect_info(game, node)
    result, last_player, winning_color, winning_clique, num_moves = end_game_eval(game)
    if head_start is not None:
        num_moves = i
    if result == 'D':
        p1_reward = p2_reward = 0
    else:
        # the last player to make a play was the loser of the game.
        p1_reward = -1 if last_player == 'player1' else 1
        p2_reward = -p1_reward
    collector1.complete_episode(p1_reward)
    collector2.complete_episode(p2_reward)
    return result, num_moves

def parallel_self_play_games(trained_model, encoder_name,
                             graph_order, clique_orders,
                             MCTS_rounds, MCTS_temps,
                             num_batches, games_per_batch, exp_dir, worker_ID,
                             head_start = None, first_move_random = False):
    model = load_model(f'{trained_model}')
    encoder = Encoder.get_encoder_by_name(encoder_name, graph_order)
    board = Board(nx.complete_graph(graph_order))
    player1 = ZeroAgent(model, encoder, MCTS_rounds, MCTS_temps[0])
    player2 = ZeroAgent(model, encoder, MCTS_rounds, MCTS_temps[1])
    num_wins = 0
    total_moves = 0
    long_games = 0
    num_games = num_batches * games_per_batch
    for i in range(num_batches):
        collector1 = ZeroExperienceCollector()
        collector2 = ZeroExperienceCollector()
        exp_tag = f'worker{worker_ID}_batch{i+1}'
        for i in range(games_per_batch):  
            player1.set_collector(collector1)
            player2.set_collector(collector2)
            sim = game_sim(board, clique_orders, player1, collector1, player2, collector2, head_start, first_move_random)
            result = sim[0]
            num_moves = sim[1]
            if num_moves == 10:
                long_games +=1 
            if result == 'win':
                num_wins +=1
            total_moves += num_moves
        experience = combine_experience([collector1, collector2])
        save_experience(experience, exp_dir, exp_tag)
    print(f'num wins out of {num_games} games: {num_wins}')
    print(f'long games: {long_games}')
    print(f'average number of moves per game: {total_moves/num_games}')


def combine_files(full_exp_dir):
    directory = full_exp_dir
    os.mkdir(f'{directory}/combined')
    files = os.listdir(directory)
    # print(files)
    # input('[enter]')
    states = [file for file in files if 'states' in file]
    state_files = [f'{directory}/{state}' for state in states]
    for file in state_files:
        print(file)
    # input('[enter]')
    rewards = [file for file in files if 'rewards' in file]
    reward_files = [f'{directory}/{reward}' for reward in rewards]
    visits = [file for file in files if 'visits' in file]
    visit_files = [f'{directory}/{visit}' for visit in visits]
    combined_states = np.concatenate([np.load(state)
                                      for state in state_files])
    combined_visits = np.concatenate([np.load(visit)
                                      for visit in visit_files])
    combined_rewards = np.concatenate([np.load(reward)
                                       for reward in reward_files])
    np.save(f'{directory}/combined/combined_states.npy', combined_states)
    np.save(f'{directory}/combined/combined_rewards.npy', combined_rewards)
    np.save(f'{directory}/combined/combined_visits.npy', combined_visits)