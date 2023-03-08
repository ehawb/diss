import networkx as nx
import dill
import random
from botparts.board import Board, GameState
from botparts.gametypes import Player
from botparts.board_utils import print_board, print_move
# from botparts.agent.naive import RandomBot
from utils.random_string import random_string

def end_game_eval(game):
    last_player = game.player.other()
    if last_player == Player.p1:
        last_player = 'player1'
    else:
        last_player = 'player2'
    result = 'D'
    num_red = len(game.red_subgraph.edges)
    num_blue = len(game.blue_subgraph.edges)
    num_moves = num_red + num_blue
    winning_color = None
    winning_clique = ()
    red_cliques = game.red_cliques
    winning_red_clique_order = game.red_clique_order
    blue_cliques = game.blue_cliques
    winning_blue_clique_order = game.blue_clique_order
    try:
        largest_red_clique = max(red_cliques, key = len)
    except ValueError:
        largest_red_clique = ()
    if len(largest_red_clique) >= winning_red_clique_order:
        winning_color = 'red'
        winning_clique = largest_red_clique
        result = 'W'
    try:
        largest_blue_clique = max(blue_cliques, key = len)
    except ValueError:
        largest_blue_clique = ()
    if len(largest_blue_clique) >= winning_blue_clique_order:
            winning_color = 'blue'
            winning_clique = largest_blue_clique
            result = 'W'
    # if all edges were colored but the game ultimately resulted in a loss  
    return(result, last_player, winning_color, winning_clique, num_moves)

def game_info(game):
    print(f'red cliques: {game.red_cliques}')
    print(f'red edges: {game.red_subgraph.edges}')
    print(f'blue cliques: {game.blue_cliques}')
    print(f'blue edges: {game.blue_subgraph.edges}')
    print(f'p1 edges: {game.p1_edges}')
    print(f'p2 edges: {game.p2_edges}')
    num_red = len(list(game.red_subgraph.edges))
    num_blue = len(list(game.blue_subgraph.edges))
    return num_red, num_blue



def simulate_game(solitaire_bot, board_size, clique_order, graph = None):
    result = 'WIN' # set a default result (assuming someone wins the game)
    interesting_game_directory = f'interesting_games/{board_size}' # a place to save interesting results
    gamestates = []
    if graph is None:
        graph = nx.complete_graph(n = board_size)
    num_edges = graph.number_of_edges()
    board = Board(graph)
    game = GameState.new_game(board, clique_order = clique_order)
    # agents = {Player: solitaire_bot}
    gamestates.append(game)
    num_moves = 0
    while not game.is_over():
        next_move = solitaire_bot.select_move(game)
        # print_move(game.player.color, next_move)
        game = game.apply_move(next_move)
        gamestates.append(game)
        num_moves +=1
    result, winning_color, winning_clique = end_game_eval(game)
    if result == 'draw':
        interesting_game_directory = f'{interesting_game_directory}/{result}'
        save_ID = random_string(6, 4)
        filename = f'{result}_G{board_size}C{clique_order}_{save_ID}'
        with open(f'{interesting_game_directory}/{filename}.pickle', 'wb') as file:
            dill.dump(gamestates, file)
        print('The game ended in a draw.')
        return result
    if num_moves == num_edges:
        result = 'LONG_GAME'
        interesting_game_directory = f'{interesting_game_directory}/{result}'
        save_ID = random_string(6, 4)
        filename = f'{result}_G{board_size}C{clique_order}_{save_ID}'
        with open(f'{interesting_game_directory}/{filename}.pickle', 'wb') as file:
            dill.dump(gamestates, file)
    if winning_color == 'red':
        winning_clique_order = game.red_clique_order
    else:
        winning_clique_order = game.blue_clique_order
    # print(f'{winning_color} clique of size {winning_clique_order}: {winning_clique}')
    return result

def simulate_and_print_game(solitaire_bot, board_size, clique_order, graph = None):
    result = 'lose' # set a default result (assume the game is lost)
    interesting_game_directory = f'interesting_games/{board_size}' # a place to save interesting results
    gamestates = []
    if graph is None:
        graph = nx.complete_graph(n = board_size)
    num_edges = graph.number_of_edges()
    board = Board(graph)
    game = GameState.new_game(board, clique_order = clique_order)
    # agents = {Player: solitaire_bot}
    gamestates.append(game)
    num_moves = 0
    while not game.is_over():
        next_move = solitaire_bot.select_move(game)
        # print_move(game.player.color, next_move)
        game = game.apply_move(next_move)
        gamestates.append(game)
        print_board(game.board)
        num_moves +=1
    result, winning_color, winning_clique = end_game_eval(game)
    num_red_edges = game.red_subgraph.number_of_edges()
    num_blue_edges = game.blue_subgraph.number_of_edges()
    edge_counts = (num_red_edges, num_blue_edges)
    if result == 'win':
        int_result = 'draw'
        interesting_game_directory = f'{interesting_game_directory}/{int_result}'
        save_ID = random_string(6, 4)
        filename = f'{result}_G{board_size}C{clique_order}_{save_ID}'
        with open(f'{interesting_game_directory}/{filename}.pickle', 'wb') as file:
            dill.dump(gamestates, file)
        print('The game ended in a draw.')
        winning_color = None
        return (result, clique_order, winning_color, edge_counts, num_edges)
    if num_moves == num_edges:
        int_result = 'long_game'
        interesting_game_directory = f'{interesting_game_directory}/{int_result}'
        save_ID = random_string(6, 4)
        filename = f'{result}_G{board_size}C{clique_order}_{save_ID}'
        with open(f'{interesting_game_directory}/{filename}.pickle', 'wb') as file:
            dill.dump(gamestates, file)
    # print(f'{winning_color} clique of size {winning_clique_order}: {winning_clique}')
    return (result, clique_order, winning_color, edge_counts, num_edges)
    return result

def self_play_game(solitaire_bot, board_size, clique_order, graph = None):
    result = 'lose' # set a default result (assume the game is lost)
    interesting_game_directory = f'interesting_games/{board_size}' # a place to save interesting results
    gamestates = []
    if graph is None:
        graph = nx.complete_graph(n = board_size)
    num_edges = graph.number_of_edges()
    board = Board(graph)
    game = GameState.new_game(board, clique_order = clique_order)
    # agents = {Player: solitaire_bot}
    gamestates.append(game)
    num_moves = 0
    while not game.is_over():
        next_move = solitaire_bot.select_move(game)
        # print_move(game.player.color, next_move)
        game = game.apply_move(next_move)
        gamestates.append(game)
        num_moves +=1
    result, winning_color, winning_clique = end_game_eval(game)
    num_red_edges = game.red_subgraph.number_of_edges()
    num_blue_edges = game.blue_subgraph.number_of_edges()
    edge_counts = (num_red_edges, num_blue_edges)
    if result == 'win':
        int_result = 'draw'
        interesting_game_directory = f'{interesting_game_directory}/{int_result}'
        save_ID = random_string(6, 4)
        filename = f'{result}_G{board_size}C{clique_order}_{save_ID}'
        with open(f'{interesting_game_directory}/{filename}.pickle', 'wb') as file:
            dill.dump(gamestates, file)
        print('The game ended in a draw.')
        winning_color = None
        return (result, clique_order, winning_color, edge_counts, num_edges)
    if num_moves == num_edges:
        int_result = 'long_game'
        interesting_game_directory = f'{interesting_game_directory}/{int_result}'
        save_ID = random_string(6, 4)
        filename = f'{result}_G{board_size}C{clique_order}_{save_ID}'
        with open(f'{interesting_game_directory}/{filename}.pickle', 'wb') as file:
            dill.dump(gamestates, file)
    # print(f'{winning_color} clique of size {winning_clique_order}: {winning_clique}')
    return (result, clique_order, winning_color, edge_counts, num_edges)

def selfplayAC_game(red_player, blue_player, 
                  board_size, clique_order, graph = None):
    result = 'WIN' # set a default result (assuming someone wins the game)
    interesting_game_directory = f'interesting_games/{board_size}' # a place to save interesting results
    gamestates = []
    if graph is None:
        # print(f'initializing new graph in selfplayAC_game')
        graph = nx.complete_graph(n = board_size)
    num_edges = graph.number_of_edges()
    board = Board(graph)
    game = GameState.new_game(board, clique_order = clique_order)
    # print(f'started a new gamestate: {game.__dict__}')
    agents = {
        Player.red: red_player,
        Player.blue: blue_player
        }
    gamestates.append(game)
    num_moves = 0
    moves = []
    # print('starting a game in the selfplayAC_game script.')
    while not game.is_over():
        if num_moves < (num_edges/5):
            # pick randomly
            # print('picking a random move.')
            agents[game.player].set_temperature(1.0)
        else:
            # favor the best-looking move
            # print('picking the best looking move.')
            agents[game.player].set_temperature(0.05)
        next_move = agents[game.player].select_move(game)
        game = game.apply_move(next_move)
        gamestates.append(game)
        moves.append(next_move)
        num_moves +=1
        # print(f'red cliques: {game.red_cliques}')
        # print(f'blue cliques: {game.blue_cliques}')
    num_red_edges = game.red_subgraph.number_of_edges()
    num_blue_edges = game.blue_subgraph.number_of_edges()
    edge_counts = (num_red_edges, num_blue_edges)
    if game.last_move is not None:
        winner = game.player
    else:
        winner = game.player.other
    loser = winner.other
    winning_color = loser.color()
    if winning_color == 'red':
        winning_clique_order = game.red_clique_order
        monochromatic_cliques = game.red_cliques
    if winning_color == 'blue':
        winning_clique_order = game.blue_clique_order
        monochromatic_cliques = game.blue_cliques
    if len(monochromatic_cliques) == 0:
        winner = None
        result = 'DRAW'
        interesting_game_directory = f'{interesting_game_directory}/{result}'
        save_ID = random_string(6, 4)
        filename = f'{result}_G{board_size}C{clique_order}_{save_ID}'
        with open(f'{interesting_game_directory}/{filename}.pickle', 'wb') as file:
            dill.dump(gamestates, file)
        # print('The game ended in a draw.')
        return (winner, monochromatic_cliques, result, edge_counts, (game.red_clique_order, game.blue_clique_order), moves)
    longest_clique = max(monochromatic_cliques, key=len)
    if len(longest_clique) < winning_clique_order:
        winner = None
        result = 'DRAW'
        interesting_game_directory = f'{interesting_game_directory}/{result}'
        save_ID = random_string(6, 4)
        filename = f'{result}_G{board_size}C{clique_order}_{save_ID}'
        # with open(f'{interesting_game_directory}/{filename}.pickle', 'wb') as file:
        #     dill.dump(gamestates, file)
        # print('The game ended in a draw.')
        return (winner, monochromatic_cliques, result, edge_counts, (game.red_clique_order, game.blue_clique_order))
    if num_moves == num_edges:
        result = 'LONG_GAME'
        interesting_game_directory = f'{interesting_game_directory}/{result}'
        save_ID = random_string(6, 4)
        filename = f'{result}_G{board_size}C{clique_order}_{save_ID}'
        with open(f'{interesting_game_directory}/{filename}.pickle', 'wb') as file:
            dill.dump(gamestates, file)
    # print(f'{winner.color().capitalize()} wins. \n {winning_color.capitalize()} clique of size {winning_clique_order}: {longest_clique}')
    return (winner, monochromatic_cliques, result, edge_counts, (game.red_clique_order, game.blue_clique_order), moves)
