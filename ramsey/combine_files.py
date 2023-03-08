import os
import numpy as np


def combine_files(exp_dir, address = None):
    """ exp_dir is the experience folder where separate files are stored.
    Alternatively, give a full address for where experience is stored (for
    working with an external drive, e.g.)
    
    """
    if address is not None:
        directory = address
    else:
        directory = f'experience/{exp_dir}'
    os.mkdir(f'{directory}/combined')
    files = os.listdir(directory)
    # print(files)
    # input('[enter]')
    states = [file for file in files if 'states' in file]
    state_files = [f'{directory}/{state}' for state in states]
    # input('[enter]')
    rewards = [file for file in files if 'rewards' in file]
    reward_files = [f'{directory}/{reward}' for reward in rewards]
    visits = [file for file in files if 'visits' in file]
    visit_files = [f'{directory}/{visit}' for visit in visits]
    for i in range(len(visit_files)):
        print(state_files[i], reward_files[i], visit_files[i])
    input('[enter]')

    combined_states = np.concatenate([np.load(state)
                                      for state in state_files])
    combined_visits = np.concatenate([np.load(visit)
                                      for visit in visit_files])
    combined_rewards = np.concatenate([np.load(reward)
                                       for reward in reward_files])
    np.save(f'{directory}/combined/combined_states.npy', combined_states)
    np.save(f'{directory}/combined/combined_rewards.npy', combined_rewards)
    np.save(f'{directory}/combined/combined_visits.npy', combined_visits)
    
combine_files('14Apr2021_0818_3600games')