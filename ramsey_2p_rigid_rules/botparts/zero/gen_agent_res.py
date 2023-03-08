import numpy as np
from copy import deepcopy, copy
from tensorflow.keras.optimizers import SGD
from botparts.agent.base import Agent
from botparts.zero.agent_utils import get_indices, get_edges, get_priors
from botparts.zero.agent_utils import host_edge_list, ends_game
from botparts.board import Move
from random import choice
from random import sample
from botparts.encoders.experience import ZeroExperienceBuffer
from sklearn.utils import shuffle
import time

class Branch:
    def __init__(self, prior):
        self.prior = prior
        self.visit_count = 0
        self.total_value = 0.0

class ZeroTreeNode:
    def __init__(self, state, value, priors, parent, last_move):
        self.state = state
        self.value = value
        self.parent = parent
        self.last_move = last_move
        self.total_visit_count = 1
        self.branches = {}
        if not self.is_node_terminal():
            for move, p in priors.items():
                if state.is_valid_move(move):
                # print(f'{move} is valid from this gamestate.')
                    self.branches[move] = Branch(p)
        else:
            # print(f'terminal node.')
            self.children = {}
        self.children = {}
    
    def is_node_terminal(self):
        """Decides if a node is terminal. In this case, no children should be added."""
        red_order = self.state.red_clique_order
        blue_order = self.state.blue_clique_order
        max_red = 0
        max_blue = 0
        if self.last_move is None:
            return False
        else:
            red_check = self.state.check_monochromatic_cliques(self.last_move, 'red')
            try:
                max_red = max(red_check, key = len)
                max_red = len(max_red)
            except ValueError:
                max_red = 0
            blue_check = self.state.check_monochromatic_cliques(self.last_move, 'blue')
            try:
                max_blue = max(blue_check, key = len)
                max_blue = len(max_blue)
            except ValueError:
                max_blue = 0
            if max_red == red_order:
                # print('red clique. terminal node')
                return True
            elif max_blue == blue_order:
                # print('blue clique. terminal node')
                return True
            else:
                return False

    def __str__(self):
        return f'AZNode[parent: {self.parent} | value: {self.value}]'
    
    def moves(self):
        # returns a list of all possible moves from this node
        return self.branches.keys()
    
    def add_child(self, move, child_node):
        self.children[move] = child_node
    
    def has_child(self, move):
        # print(f'checking to see if move {move} of type {type(move)} is in children.')
        # print(f'children: {self.children}')
        check_over = self.state.is_over()
        if check_over:
            # print(f'no children -- terminal gamestate.')
            return False
        return move in self.children
    
    def get_child(self, move):
        # print(f'getting child of {move}, number of children: {len(self.children)}')
        return self.children[move]
    
    def expected_value(self, move):
        branch = self.branches[move]
        if branch.visit_count == 0:
            return 0.0
        expected_value = branch.total_value / branch.visit_count
        check = isinstance(expected_value, float)
        if not check:
            print('something happened in expected value.')
            print(f' total value: {branch.total_value}')
            print(f'visit count: {branch.visit_count}')
            input('[enter]')
        return branch.total_value / branch.visit_count
    
    def prior(self, move):
        return self.branches[move].prior
    
    def visit_count(self, move):
        # print(f'checking visit_count of move {move}')
        if move in self.branches:
            return self.branches[move].visit_count
        return 0
    
    def record_visit(self, move, value):
        # print(f'move type: {type(move)} value: {value}')
        # print(f'recording visit to {move}')
        self.total_visit_count += 1
        self.branches[move].visit_count += 1
        self.branches[move].total_value += value
        # print(f'   total visits to this node: {self.branches[move].visit_count}')
        # print(f'   node value after adding {value}: {self.branches[move].total_value}')
    
class ZeroAgent(Agent):
    def __init__(self, model, encoder, rounds_per_move = 250, c = .5):
        self.model = model
        self.encoder = encoder
        self.collector = None
        self.num_rounds = rounds_per_move
        self.c = c
        
    def game_info(self, game):
        print(f'      red cliques: {game.red_cliques}')
        print(f'      red edges: {game.red_subgraph.edges}')
        print(f'      blue cliques: {game.blue_cliques}')
        print(f'      blue edges: {game.blue_subgraph.edges}')
        print(f'      p1 edges: {game.p1_edges}')
        print(f'      p2 edges: {game.p2_edges}')
        print(f'      next player: {game.player}')
        
    def select_move(self, game_state):
        start = time.time()
        game_state = deepcopy(game_state)
        Root = self.create_node(game_state)
        root = deepcopy(Root)
        root_player = game_state.player
        # print(f'select move, root {root} type: {type(root)}')
        for i in range(self.num_rounds):
            # input(f'------------------------ round {i+1} of {self.num_rounds}. [enter] ------------------------')
            # print(f'------------------------ round {i+1} of {self.num_rounds}. ------------------------')
            node = root
            # print(' ********** info about the root game state:')
            # self.game_info(node.state)
            next_move = self.select_branch(node)
            # input(f'selected move: {next_move} [enter]')
            is_over = False
            # print(f'selected branch {next_move}')
            # print('-----walking down tree')
            # input('walking down tree. [enter]')
            while node.has_child(next_move):
                # input('walking down tree. [enter]')
                # print(f'     walking down tree.......')
                # print(f'{next_move} has a child:')
                # print(f'    game info -------')
                # self.game_info(node.state)
                node = node.get_child(next_move)
                # print(f'****** selecting a branch within the tree walk.')
                # print(f'how many moves from this node? {len(node.moves())}')
                try:
                    next_move = self.select_branch(node)
                    # print(f'                  exploring next move: {next_move}.')
                except:
                    is_over = True
                    # print('before backing up:')
                    # self.game_info(node.state)
                    winner = node.state.player
                    # print('info about terminal gamestate:')
                    # self.game_info(node.state)
                    # print(f'winner of that game: {winner}')
                    # undo that last step...
                    child_node = node
                    node = node.parent
                    # node.value = 1 if winner == root_player else -1
                    next_move = next_move
                    # print(f'assign a value of {node.value} to that node.')
                    # input('[enter]')
                    # print(f'  went back to the parent. the next move is {next_move}')
                    # print('******************** no moves -- leave the loop.')
                    break
            # print(f'[][][][][] making a new state with {next_move} type {type(next_move)} [][][][][]')
            if not is_over:
                node_state = deepcopy(node.state)
                new_state = node_state.apply_move(Move.play(next_move), update = True)
                # print(f'%% a new state was created after applying a move {next_move}. info:')
                # self.game_info(new_state)
                # print(f'%% info again:')
                # self.game_info(new_state)
                child_node = self.create_node(
                new_state, move = next_move, parent = node)
                # print(f'%% info about the new state after creating node:')
                # self.game_info(new_state)
            else:
                child_node.value = -1
                # print(""" ======
                      # ======
                      # ======
                      # ======""")
                # print(f'child node info:')
                # self.game_info(child_node.state)
                # input(f'value assigned: {child_node.value} [enter]')# no new child to create; this is just the child.
            move = next_move
            # print(f'move: {next_move}')
            value = - 1 * child_node.value
            # print(f'node value: {value}')
            # print('----- walking back up tree.')
            # input('walking back up tree. [enter]')
            while node is not None:
                # print('     -- walking back up tree. [enter]')
                # move_idx = self.encoder.encode_move(move, game_state)
                # print(f'found move idx {move_idx} for move {move}')
                node.record_visit(move, value)
                move = node.last_move
                node = node.parent
                value = -1 * value 
        if self.collector is not None:
            # print(f'recording info about the move.')
            self.collect_info(game_state, root)
        # print(f'visit_counts: {visit_counts}')
        for move in root.moves():
            print(f'{move} ---> {root.visit_count(move)}')
        # input('[enter]')
        # most_visits = max(root.moves(), key = root.visit_count)
        max_visit_count = max([root.visit_count(move) for move in root.moves()])
        max_visits = []
        for move in root.moves():
            if root.visit_count(move) == max_visit_count:
                max_visits.append(move)
        
        # print(f'there are {len(max_visits)} moves with {max_visit_count} visits: {max_visits}')
        most_visits = choice(max_visits)
        end = time.time()
        total = end - start
        print(f'spent {total} seconds selecting a move.')
        # print(f'-- agent move selected: {most_visits}')
        # print(f'returning {Move.play(most_visits)}')

        return Move.play(most_visits)
    
    def collect_info(self, game_state, root):    
        root_state_tensor = self.encoder.encode(game_state)
        symmetric_root_tensor = self.encoder.symmetric_encoding(game_state)
        # print(f'root state tensor: \n {root_state_tensor}')
        # print(f'symmetric root state tensor: \n {symmetric_root_tensor}')
        # input('[enter]')
        visit_counts = np.array([
            root.visit_count(
                self.encoder.decode_edge_index(index, game_state))
            for index in range(self.encoder.num_points())
            ])
        num_edges = len(game_state.board.edges)
        symmetric_visit_shift = int(num_edges)
        symmetric_visit_counts = np.roll(visit_counts, symmetric_visit_shift)
        # print(f'visit counts: {visit_counts}')
        # print(f'symmetric visit counts: {symmetric_visit_counts}')
        n = game_state.board.graph.order()
        shifted_states = []
        shifted_visits = []
        # augment the data set:
        shifts = range(1, n)
        # get shifted states
        for shift in shifts:
            shifted_state = self.encoder.relabeled_encoding(game_state, shift)
            # get shifted visits
            shifted_visit = self.shift_visit_counts(visit_counts, shift, n, game_state)
            shifted_states.append(shifted_state)
            shifted_visits.append(shifted_visit)
        # input('sending info to collector... [enter]')
        self.collector.record_decision(
            root_state_tensor, visit_counts,
            symmetric_root_tensor, symmetric_visit_counts, shifted_states, shifted_visits)    
    
    def shift_visit_counts(self, visits, shift, n, game_state):
        visit_counts = visits
        colored_edge_list = game_state.colored_edge_list
        # input(f'colored edge list: \n {colored_edge_list}')
        diff = n-shift
        shifted_visits = []
        for edge in colored_edge_list:
            u, v = edge[0], edge[1]
            color_ind = edge[2]
            u1, v1 = (u+diff)%n, (v+diff)%n
            if u1 > v1:
                u0, v0 = v1, u1
            else:
                u0, v0 = u1, v1
            edge_preimage = u0, v0, color_ind
            preimage_index = self.encoder.encode_move(edge_preimage, game_state)
            # print(f'got preimage index of {preimage_index} for preimage {edge_preimage}')
            preimage_visit = visit_counts[preimage_index]
            shifted_visits.append(preimage_visit)
        shifted_visits = np.array(shifted_visits)
        # input(f'returning shifted visits of type {type(shifted_visits)}: {shifted_visits}')
        return shifted_visits
            
            
        
    def set_collector(self, collector):
        self.collector = collector
        
    def select_branch(self, node):
        # print(f'~~~ selecting branch from node {node.last_move}. info about the node:')
        # self.game_info(node.state)
        total_n = node.total_visit_count
        is_over = node.state.is_over()
        # print(f'is over: {is_over}')
        # print(f'total visit count for node: {total_n}')
        def score_branch(move):
            q = node.expected_value(move)
            p = node.prior(move)
            n = node.visit_count(move)
            score = q + self.c * p * np.sqrt(total_n) / (n+1)
            # input(f'{move} || score: {score} | expected value: {q} | prior: {p} | visit count: {n}')
            return score
        # print(f'find high score branch. number of possible moves: {len(node.moves())}')
        try:
            moves = list(node.moves())
            # input(f'moves: {moves}')                  
            high_score = max([score_branch(move) for move in moves])
            # input(f'high score: {high_score}')
            high_score_moves = []
            for move in moves:
                if score_branch(move) == high_score:
                    high_score_moves.append(move)
            high_score_branch = choice(high_score_moves)
                # high_score_branch = max(better_moves, key = score_branch)
        except ValueError:
            # print('value error??')
            # print('no high score branch.')
            # print(f'value error. info:')
            # print(f'number of moves from this node: {len(node.moves())}')
            # self.game_info(node.state)
            # input('[enter]')
            pass
        # input(f'returning high score branch {high_score_branch} with score: {high_score}')
        return high_score_branch
    
    def create_node(self, game_state, move = None, parent = None):
        # print(f'creating node for move {move}')
        # print(f'---- info about the game state passed into the create_node:')
        # self.game_info(game_state)
        state_tensor = [] 
        # print('info again without encoder doing stuff:')
        # self.game_info(game_state)
        # input('[stop the code now.]')
        to_encode = deepcopy(game_state)
        state_tensor = self.encoder.encode(to_encode)
        # print(f'info after the encoder did stuff:')
        # self.game_info(game_state)
        # input('[stop the code???????]')
        model_input = np.array([state_tensor])
        priors, values = self.model.predict(model_input)
        num_possible_moves = len(game_state.colored_edge_list)
        num_edges = num_possible_moves//2
        # print(f'priors: {priors}')
        # print(f'values: {values}')
        # print('called create node to create priors.')
        priors = priors[0]
        # print(f'original priors: {priors}')
        # only take the priors relevant to this particular graph
        host_edges = host_edge_list()
        # print(f'host edges: {host_edges}')
        relevant_edges = game_state.colored_edge_list
        # print(f'relevant edges: {relevant_edges}')
        indices = get_indices(relevant_edges, host_edges)
        # print(f'indices: {indices}')
        relevant_priors = get_priors(priors, indices)
        # input(f'relevant priors: {relevant_priors}  [enter]')
        # print(f'priors: {priors} length: {len(priors)}')
        value = values[0][0]
        # print(f'pulled priors {priors} and value {value}')
        move_priors = {
            self.encoder.decode_edge_index(index, game_state): p 
            for index, p in enumerate(relevant_priors)
            }
        # for move, prior in move_priors.items():
            # print(f'{move} ---> {prior}')
        new_node = ZeroTreeNode(
            game_state,
            value,
            move_priors,
            parent,
            move)
        # print('new child node info:')
        # self.game_info(new_node.state)
        if parent is not None:
            # print('adding child.')
            parent.add_child(move, new_node)
        return new_node
    
    def train(self, experience, learning_rate, batch_size, model_ID):
        exp = shuffle_game_data(experience)
        num_examples = exp.states.shape[0]
        model_input = exp.states
        visit_sums = np.sum(
            exp.visit_counts, axis=1).reshape((num_examples, 1))
        action_target = exp.visit_counts / visit_sums
        value_target = exp.rewards
        print(f'The agent is training on {num_examples} examples of game states.')
        print(f'The action target is {action_target}.')
        print(f'The value target is {value_target}.')
        self.model.compile(
            SGD(lr = learning_rate),
            loss = ['categorical_crossentropy', 'mse'])
        history = self.model.fit(model_input, [action_target, value_target],
                       batch_size = batch_size)
        self.model.save(f'models/{model_ID}')
        self.model.summary()
        
        print(f'This model was saved as {model_ID}')
        print(f'Learning rate: {learning_rate}')
        print(f'Batch size: {batch_size}')
        print(f'MCTS rounds per move: {self.num_rounds}')
        print(f'MCTS temperature: {self.c}')
        return history

def shuffle_game_data(experience):
    num_examples = experience.states.shape[0]
    states = experience.states
    rewards = experience.rewards
    visits = experience.visit_counts
    shuff_states, shuff_rewards, shuff_visits = shuffle(states, rewards, visits, random_state = 2021)
    shuff_exp = ZeroExperienceBuffer(states = shuff_states,
                                     visit_counts = shuff_visits,
                                     rewards = shuff_rewards)
    return shuff_exp