import numpy as np

exp_location = 'C:/Python/ramsey_2p/experience/experiments_10Apr2021_0106_6000games/combined'

states = np.load(f'{exp_location}/combined_states.npy')
visits = np.load(f'{exp_location}/combined_visits.npy')
rewards = np.load(f'{exp_location}/combined_rewards.npy')

print(f'states shape: {states.shape}')
print(f'visits shape: {visits.shape}')
print(f'rewards shape: {rewards.shape}')