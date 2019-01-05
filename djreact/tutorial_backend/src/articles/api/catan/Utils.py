import numpy as np


def high_low_rolls(distribution):
    """
    Returns the lists of high and low probability rolls
    """
    dist = distribution.copy()
    dist[7] = 0
    high_probability_rolls = np.argwhere(np.max(dist) == dist).reshape(1, -1)
    high = high_probability_rolls.tolist()[0]
    low = [roll for roll in list(range(2, 13)) if roll not in high]
    return high, low
