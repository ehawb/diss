from tensorflow.keras.models import load_model
import networkx as nx
import sys
import numpy as np
from copy import deepcopy
from botparts.encoders.base import Encoder
from botparts.gametypes import Player
from botparts.agent.random_agent import RandomAgent
from botparts.zero.agent_main import ZeroAgent
from botparts.zero.agent_interactive import InteractiveZeroAgent
from botparts.board import GameState, Board
from utils.simulations import end_game_eval, game_info
from botparts.board_utils import print_board

np.set_printoptions(threshold = sys.maxsize)
    
def game_sim(board, clique_orders, player1, player2,
             print_settings, pause_settings, head_start = None):
    if head_start is None:
        game = GameState.new_game(
            board, clique_orders)
    else:
        game = deepcopy(head_start)
    print('------------- beginning the game. ------------- ')
    i=1
    agents = {Player.p1: player1, Player.p2 : player2}
    while not game.is_over():
        if print_settings == 'all':
            print_board(game.board)
        move = agents[game.player].select_move(game)
        game = game.apply_move(move)
        if pause_settings != 'moves':
            print(f'move {i}: {move} ')
        else:
            print(f'move {i}: {move}')
            print('recap of game so far:')
            game_info(game)
            input('[enter]')
        i +=1
    print('game over! info:')
    game_info(game)
    result, last_player, losing_color, losing_clique, num_moves = end_game_eval(game)
    print(f'The game was a {result}. The last player to make a move was {last_player}.')
    print(f'number of moves: {num_moves}')
    if print_settings in ['all', 'end']:
        print_board(game.board)
        
    return result, last_player, num_moves

def new_game_sim(board, clique_orders, player1, player2,
             print_settings, pause_settings, head_start = None, first_move_random = False):
    if head_start is None:
        game = GameState.new_game(
            board, clique_orders)
    else:
        game = deepcopy(head_start)
        game.player = Player.p1
    
    print('------------------------ beginning the game. ------------------------ ')
    i=1
    agents = {Player.p1: player1, Player.p2 : player2}
    first_node = agents[game.player].create_node(game)
    node = deepcopy(first_node)
    while not game.is_over():
        if print_settings == 'all':
            print_board(game.board)
        if i == 1:
            if first_move_random:
                move, node = agents[game.player].select_move(node, random = True)
            else:
                move, node = agents[game.player].select_move(node)
        else:
            move, node = agents[game.player].select_move(node)
        game = game.apply_move(move)
        if pause_settings != 'moves':
            print(f'move {i}: {move} ')
        else:
            print(f'move {i}: {move}')
            print('recap of game so far:')
            game_info(game)
            input('[enter]')
        i +=1
    print(f'game over! info: \n first move random? {first_move_random}')
    game_info(game)
    result, last_player, losing_color, losing_clique, num_moves = end_game_eval(game)
    print(f'The game was a {result}. The last player to make a move was {last_player}.')
    print(f'number of moves: {num_moves}')
    if print_settings in ['all', 'end']:
        print_board(game.board)
        
    return result, last_player, num_moves

def observe(player1, player2,
            graph_order, clique_orders, encoder_name,
            print_settings, pause_settings, interactive,
            num_games, head_start = None, first_move_random = False):
    board = Board(nx.complete_graph(graph_order))
    encoder = Encoder.get_encoder_by_name(encoder_name, graph_order)
    if player1 == 'random':
        player1 = RandomAgent(load_model(''), encoder)
    else:
        model, rounds, temp = player1
        p1_model = load_model(model)
        player1 = InteractiveZeroAgent(p1_model, encoder, rounds, temp) if interactive else ZeroAgent(p1_model, encoder, rounds, temp)
    if player2 == 'random':
        player2 = RandomAgent(load_model(''), encoder)
    else:
        model, rounds, temp = player2
        p2_model = load_model(model)
        player2 = InteractiveZeroAgent(p2_model, encoder, rounds, temp) if interactive else ZeroAgent(p2_model, encoder, rounds, temp)
    total_moves = 0
    p1_lose = 0
    num_draws = 0
    for i in range(num_games):
        print(f'==== game {i+1} ====')
        print(f'Graph is of order {board.graph.order()}')
        result, last_player, num_moves = new_game_sim(board, clique_orders,
                                                  player1, player2,
                                                  print_settings, pause_settings, head_start, first_move_random)
        if pause_settings in ['moves', 'games']:
            input('[enter]')
        if last_player == 'player1':
            p1_lose +=1
        total_moves += num_moves
        if result == 'D':
            num_draws +=1
    average_moves = total_moves/num_games
    print(f'number of P1 losses: {p1_lose}')
    print(f'Number of draws: {num_draws}')
    print(f'average number of moves across {num_games} games: {average_moves}')

def evaluate(q, player1, player2,
            graph_order, clique_orders, encoder_name,
            print_settings, pause_settings, interactive,
            num_games):
    board = Board(nx.complete_graph(graph_order))
    encoder = Encoder.get_encoder_by_name(encoder_name, graph_order)
    if player1 == 'random':
        player1 = RandomAgent()
    else:
        model, rounds, temp = player1
        p1_model = load_model(model)
        player1 = InteractiveZeroAgent(p1_model, encoder, rounds, temp) if interactive else ZeroAgent(p1_model, encoder, rounds, temp)
    if player2 == 'random':
        player2 = RandomAgent()
    else:
        model, rounds, temp = player2
        p2_model = load_model(model)
        player2 = InteractiveZeroAgent(p2_model, encoder, rounds, temp) if interactive else ZeroAgent(p2_model, encoder, rounds, temp)
    total_moves = 0
    p1_wins = 0
    for i in range(num_games):
        print(f'==== game {i+1} ====')
        result, last_player, num_moves = new_game_sim(board, clique_orders,
                                                  player1, player2,
                                                  print_settings, pause_settings)
        if pause_settings in ['moves', 'games']:
            input('[enter]')
        if last_player == 'player1':
            p1_wins +=1
        total_moves += num_moves
    average_moves = total_moves/num_games
    print(f'number of P1 wins: {p1_wins}')
    print(f'average number of moves across {num_games} games: {average_moves}')
    q.put([p1_wins, total_moves])