import numpy as np 

rewards = np.load('C:/Users/emily/ramsey/ramsey_2p_rigid_rules/experience/30jan2023_1007_2000games/combined/combined_rewards.npy')
#print(rewards[-1])
visits = np.load('C:/Users/emily/ramsey/ramsey_2p_rigid_rules/experience/30jan2023_1007_2000games/combined/combined_visits.npy')
#print(visits[-1])
states =  np.load('C:/Users/emily/ramsey/ramsey_2p_rigid_rules/experience/30jan2023_1007_2000games/combined/combined_states.npy')
states

num_examples = states.shape[0]
visit_sums = np.sum(visits, axis=1).reshape((num_examples, 1))
for i in range(num_examples):
    if visit_sums[i] == 0:
        visit_sums[i] = 1
action_target = visits / visit_sums