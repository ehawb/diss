import numpy as np 

class ZeroExperienceCollector:
    def __init__(self):
        self.states = []
        self.visit_counts = []
        self.rewards = []
        self._current_episode_states = []
        self._current_episode_visit_counts = []
        self._current_episode_symmetric_states = []
        self._current_episode_symmetric_visit_counts = []
    
    def reset(self):
        self.states = []
        self.visit_counts = []
        self.rewards = []
        self._current_episode_states = []
        self._current_episode_visit_counts = []
        self._current_episode_symmetric_states = []
        self._current_episode_symmetric_visit_counts = []        
    
    def begin_episode(self):
        self._current_episode_states = []
        self._current_episode_visit_counts = []
    
    def record_decision(self, state, visit_counts): 
        self._current_episode_states.append(state)
        self._current_episode_visit_counts.append(visit_counts)
        
    def complete_episode(self, reward):
        num_states = len(self._current_episode_states)
        num_symmetric_states = len(self._current_episode_symmetric_states)
        self.states += self._current_episode_states
        self.visit_counts += self._current_episode_visit_counts
        self.rewards += [reward for _ in range(num_states)]
        self._current_episode_states = []
        self._current_episode_visit_counts = []
        # now do the same for the symmetric states:
        self.states += self._current_episode_symmetric_states
        self.visit_counts += self._current_episode_symmetric_visit_counts
        self.rewards += [reward for _ in range(num_symmetric_states)]
        self._current_episode_symmetric_states = []
        self._current_episode_symmetric_visit_counts = []
        test = len(self.rewards) == len(self.states) == len(self.visit_counts)
        if not test:
            print('error -- number of rewards, states, visit counts not equal')
            input('[enter]')

class ZeroExperienceBuffer:
    def __init__(self, states, visit_counts, rewards):
        self.states = states
        self.visit_counts = visit_counts
        self.rewards = rewards

    def serialize(self, h5file):
        h5file.create_group('experience')
        h5file['experience'].create_dataset(
            'states', data=self.states)
        h5file['experience'].create_dataset(
            'visit_counts', data=self.visit_counts)
        h5file['experience'].create_dataset(
            'rewards', data=self.rewards)


def combine_experience(collectors):
    combined_states = np.concatenate([np.array(c.states) for c in collectors])
    combined_visit_counts = np.concatenate([np.array(c.visit_counts) for c in collectors])
    combined_rewards = np.concatenate([np.array(c.rewards) for c in collectors])

    return ZeroExperienceBuffer(
        combined_states,
        combined_visit_counts,
        combined_rewards)

def save_experience(experience, exp_dir, exp_tag):
    np.save(f'{exp_dir}/{exp_tag}_states', experience.states)
    np.save(f'{exp_dir}/{exp_tag}_visits', experience.visit_counts)
    np.save(f'{exp_dir}/{exp_tag}_rewards', experience.rewards)

def load_experience(h5file):
    return ZeroExperienceBuffer(
        states=np.array(h5file['experience']['states']),
        visit_counts=np.array(h5file['experience']['visit_counts']),
        rewards=np.array(h5file['experience']['rewards']))