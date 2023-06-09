import networkx as nx
import numpy as np
import os
from tensorflow.keras.models import load_model
from datetime import date
from botparts.encoders.base import Encoder
from botparts.encoders.experience import ZeroExperienceCollector, ZeroExperienceBuffer
from botparts.zero.agent_main import ZeroAgent
from botparts.board import Board

exp_location = 'C:/users/emily/diss_repo/ramsey/experience/27Jan2023_1648_2000games/combined'
model_save_dir = 'C:/users/emily/diss_repo/ramsey/models'
model_name = 'initmodel_K5_3_3'

batch_size = 512
learning_rate = 0.002

graph_order = 5
clique_order = 3
encoder_name = 'k3_encoder'
MCTS_rounds = 250
MCTS_temp = 0.2

################################################################################
################################################################################
##################### leave this stuff alone :) ################################
################################################################################
################################################################################
board = Board(nx.complete_graph(graph_order))
encoder = Encoder.get_encoder_by_name(encoder_name, graph_order)
date = str(date.today())
date = date.replace('-', '_')
lr__ = str(learning_rate).replace('0.', '')
model_ID = f'{date}_{lr__}_{batch_size}'


model = load_model(f"{model_save_dir}/{model_name}")
try:
    os.mkdir(f'{model_save_dir}/{model_ID}')
except:
    pass
#%% game setup (leave this part alone)
collector = ZeroExperienceCollector()
solitaire_agent = ZeroAgent(model, encoder, MCTS_rounds, MCTS_temp)
# high value of c: more volatile search
solitaire_agent.set_collector(collector)
states_ = f'{exp_location}/combined_states.npy'
visits_ = f'{exp_location}/combined_visits.npy'
rewards_ = f'{exp_location}/combined_rewards.npy'
states = np.load(states_)
visits = np.load(visits_)
rewards = np.load(rewards_)
exp = ZeroExperienceBuffer(states, visits, rewards)
history = solitaire_agent.train(exp, learning_rate, batch_size, model_ID, model_save_dir)
print(f'model ID: {model_ID}')
