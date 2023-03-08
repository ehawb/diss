from botparts.agent.base import Agent
import numpy as np
from copy import deepcopy, copy
from tensorflow.keras.optimizers import SGD
from botparts.agent.base import Agent
from botparts.board import Move
from random import choice
from random import sample
from botparts.encoders.experience import ZeroExperienceBuffer
from sklearn.utils import shuffle
from botparts.zero.agent_main import ZeroTreeNode
from botparts.zero.agent_utils import get_indices, get_edges, get_priors
from botparts.zero.agent_utils import host_edge_list, ends_game


class RandomAgent(Agent):
    def __init__(self, opponent_model, opponent_encoder):
        
        self.model = opponent_model
        self.encoder = opponent_encoder
        
    def select_move(self, node):
        game_state = node.state
        legal_edges = game_state.legal_moves()
        agent_edge = choice(legal_edges)
        agent_color = choice([(0,), (1,)])
        agent_move = agent_edge + agent_color
        node_state = deepcopy(node.state)
        new_state = node_state.apply_move(Move.play(agent_move), update = True)
        child_node = self.create_node(new_state, move = agent_move, parent = node)
        next_node = node.get_child(agent_move)
        return Move.play(agent_move), next_node
    
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
        host_edges = host_edge_list()
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