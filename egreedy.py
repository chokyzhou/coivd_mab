import numpy as np

class EGreedy:
    """
    Implementation of EGreedy algorithm as described in Section 2 of book:
    Reinforcement Learning: An Introduction (Version 2)
    Richard S. Sutton and Andrew G. Barto
    """
    def __init__(self, k, epsilon=0.1):
        """
        Constructor of EGreedy
        :param k: [int], number of arms. 0-based indexing.
        :param epsilon: [float, default=0.1], epsilon value in range (0.0, 1.0) for exploration
        """
        self.k = k
        self.epsilon = epsilon
        self.rewards = np.asarray([0.0 for _ in range(k)])
        self.steps = np.asarray([0 for _ in range(k)])

    def reset(self):
        self.rewards = np.asarray([0.0 for _ in range(self.k)])
        self.steps = np.asarray([0 for _ in range(self.k)])

    def choose(self):
        random_number = np.random.uniform(0.0, 1, 1)[0]

        if random_number < self.epsilon:
            return np.random.choice(self.k, 1, replace=False)[0].item()
        else:
            return np.argmax(self.rewards, axis=0)

    def feedback(self, arm_id, reward):
        self.steps[arm_id] += 1
        self.rewards[arm_id] += (1 / self.steps[arm_id]) * (reward - self.rewards[arm_id])
        

    