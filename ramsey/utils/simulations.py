import networkx as nx
from botparts.gametypes import Player

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