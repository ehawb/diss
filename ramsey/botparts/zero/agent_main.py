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
        self.recent_visit_count = 0
    
    

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
                    self.branches[move] = Branch(p)
        else:
            self.children = {}
        self.children = {}
    
    def get_info(self):
        print(f"""value: {self.value}
             total visit count: {self.total_visit_count}""")
             
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
                return True
            elif max_blue == blue_order:
                return True
            else:
                return False

    def __str__(self):
        return f'AZNode[parent: {self.parent} | value: {self.value}]'
    
    def moves(self):
        # returns a list of all possible moves from this node
        return list(self.branches.keys())
    
    def add_child(self, move, child_node):
        self.children[move] = child_node
    
    def has_child(self, move):
        check_over = self.state.is_over()
        if check_over:
            return False
        return move in self.children
    
    def get_child(self, move):
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
        if move in self.branches:
            return self.branches[move].visit_count
        return 0
    
    def reset_recent_visit_count(self):
        for move in self.branches:
            self.branches[move].recent_visit_count = 0
    
    def recent_visits(self, move):
        if move in self.branches:
            return self.branches[move].recent_visit_count
        return 0
    
    def record_visit(self, move, value):
        self.total_visit_count += 1
        self.branches[move].visit_count += 1
        self.branches[move].total_value += value
        self.branches[move].recent_visit_count += 1
    
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
        
    def select_move(self, game_node, random = False):
        game_state = game_node.state
        start = time.time()
        root = game_node
        root.reset_recent_visit_count()
        root.parent = None # need to set this so don't walk too far up tree later
        root.get_info()
        for i in range(self.num_rounds):
            # start at the root
            node = root
            # select the branch with the highest UCT score
            next_move = self.select_branch(node)
            is_over = False
            # walk down the tree until a leaf is reached
            while node.has_child(next_move):
                node = node.get_child(next_move)
                try:
                    next_move = self.select_branch(node, random)
                except:
                    # if a terminal node is reached,
                    is_over = True
                    # need to back up
                    child_node = node
                    # retrace our steps
                    node = node.parent
                    # the next_move is the last move we selected before an error was thrown
                    next_move = next_move
                    break
            # if we aren't dealing with a terminal gamestate,    
            if not is_over:
                node_state = deepcopy(node.state)
                new_state = node_state.apply_move(Move.play(next_move), update = True)
                # make a new node corresponding to that gamestate
                child_node = self.create_node(
                new_state, move = next_move, parent = node)
            else:
                # otherwise, the last gamestate we landed on has a value of 1.
                # that's because it's technically Player X's turn, but the game
                # is already over; they lost when Player Y made the move to land
                # in this game state.
                # figure out if it's a win or a draw.
                rc = child_node.state.red_cliques
                bc = child_node.state.blue_cliques
                #print(f'Assessing a terminal game state with move {next_move}...')
                #print(f'Red cliques: {rc}')
                #print(f'Blue cliques: {bc}')
                if len(rc) == 0:
                    if len(bc) == 0:
                        #print(f'Found a good ending, actually: {next_move}')
                        child_node.value = 0
                else:
                    try:
                        max_red = max(rc, key=len)
                    except:
                        max_red = ()
                    try:
                        max_blue = max(bc, key=len)
                    except:
                        max_blue = ()
                    child_node.value = 1
            # now it's time to walk back up the tree.
            move = next_move
            value = - 1 * child_node.value
            original_value = value
            steps = 1
            while node is not None:
                node.record_visit(move, value)
                move = node.last_move
                node = node.parent
                value = -1 * value
                steps +=1
             #   if steps%2 == 0:
            #        value = 0.25*value
        # record the game info
        if self.collector is not None:
            self.collect_info(game_state, root)
        # display the visit counts, just to satisfy some curiosity -- which moves
        # got visited a lot?
        for move in root.moves():
            print(f'{move} -- T --> {root.visit_count(move)}')
            print(f'          R     {root.recent_visits(move)}')
        # get the highest number of visit counts that a node received
        max_visit_count = max([root.recent_visits(move) for move in root.moves()])
        # start keeping track of nodes that hit that high visit count
        max_visits = []
        for move in root.moves():
            if root.recent_visits(move) == max_visit_count:
                max_visits.append(move)
        # choose a random node with the highest number of visits (to prevent
        # repeatedly picking the same moves)
        most_visits = choice(max_visits)
        end = time.time()
        total = end - start
        next_node = root.get_child(most_visits)
        print(f'spent {total} seconds selecting a move.')
        return Move.play(most_visits), next_node
    
    def select_branch(self, node, random = False):
        total_n = node.total_visit_count
        is_over = node.state.is_over()
        def score_branch(move):
            q = node.expected_value(move)
            p = node.prior(move)
            n = node.visit_count(move)
            score = q + self.c * p * np.sqrt(total_n) / (n+1)
            return score
        try:
            high_score_moves = []
            moves = list(node.moves())
            if random:
                #print(f'Returning a random branch.')
                high_score_branch = choice(moves)
                return high_score_branch
            #print(f'{len(moves)} moves available')
            high_score = max([score_branch(move) for move in moves])
            #print(f'High score of {high_score}')
            for move in moves:
                if score_branch(move) == high_score:
                    high_score_moves.append(move)
            try:
                high_score_branch = choice(high_score_moves)
                #print('SELECTING ACTUAL HIGH SCORE BRANCH...')
            except IndexError:
                print('Making a random selection...')
                high_score_branch = choice(moves)
        except ValueError:
            pass
        return high_score_branch    
    
    def collect_info(self, game_state, root):    
        root_state_tensor = self.encoder.encode(game_state)
        #print(f'Tensor: \n {root_state_tensor}')
        #symmetric_root_tensor = self.encoder.symmetric_encoding(game_state)
        visit_counts = np.array([
            root.recent_visits(
                self.encoder.decode_edge_index(index, game_state))
            for index in range(self.encoder.num_points())
            ])
        #num_edges = len(game_state.board.edges)
        #symmetric_visit_shift = int(num_edges)
        #symmetric_visit_counts = np.roll(visit_counts, symmetric_visit_shift)
       # n = game_state.board.graph.order()
       # shifted_states = []
       # shifted_visits = []
        # augment the data set:
      #  shifts = range(1, n)
        # get shifted states
        #for shift in shifts:
            #shifted_state = self.encoder.relabeled_encoding(game_state, shift)
            # get shifted visits
            #shifted_visit = self.shift_visit_counts(visit_counts, shift, n, game_state)
            #shifted_states.append(shifted_state)
            #shifted_visits.append(shifted_visit)
        self.collector.record_decision(
            root_state_tensor, visit_counts)#,
            #symmetric_root_tensor, symmetric_visit_counts, shifted_states, shifted_visits)    
    
    def shift_visit_counts(self, visits, shift, n, game_state):
        visit_counts = visits
        colored_edge_list = game_state.colored_edge_list
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
            preimage_visit = visit_counts[preimage_index]
            shifted_visits.append(preimage_visit)
        shifted_visits = np.array(shifted_visits)
        return shifted_visits
        
    def set_collector(self, collector):
        self.collector = collector

    def create_node(self, game_state, move = None, parent = None):
        state_tensor = [] 
        to_encode = deepcopy(game_state)
        state_tensor = self.encoder.encode(to_encode)
        model_input = np.array([state_tensor])
        priors, values = self.model.predict(model_input)
        num_possible_moves = len(game_state.colored_edge_list)
        num_edges = num_possible_moves//2
        priors = priors[0]
        # only take the priors relevant to this particular graph
        host_edges = host_edge_list(game_state.board.graph.order())
        relevant_edges = game_state.colored_edge_list
        indices = get_indices(relevant_edges, host_edges)
        relevant_priors = get_priors(priors, indices)
        value = values[0][0]
        move_priors = {
            self.encoder.decode_edge_index(index, game_state): p 
            for index, p in enumerate(relevant_priors)
            }
        new_node = ZeroTreeNode(
            game_state,
            value,
            move_priors,
            parent,
            move)
        if parent is not None:
            parent.add_child(move, new_node)
        return new_node
    
    def train(self, experience, learning_rate, batch_size, model_ID, model_dir):
        exp = shuffle_game_data(experience)
        num_examples = exp.states.shape[0]
        model_input = exp.states
        visit_sums = np.sum(
            exp.visit_counts, axis=1).reshape((num_examples, 1))
        for i in range(num_examples):
            if visit_sums[i] == 0:
                visit_sums[i] = 1
        action_target = exp.visit_counts / visit_sums
        value_target = exp.rewards
        print(f'The agent is training on {num_examples} examples of game states.')
        print(f'The action target is {action_target}.')
        print(f'The value target is {value_target}.')
        self.model.compile(
            SGD(lr = learning_rate),
            loss = ['categorical_crossentropy', 'mse'])
        history = self.model.fit(x = model_input, 
                                 y = [action_target, value_target],
                       batch_size = batch_size)
        self.model.save(f'{model_dir}/{model_ID}')
        self.model.summary()
        #input('[Enter]')
        
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