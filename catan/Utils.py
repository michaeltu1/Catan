import numpy as np


def high_low_rolls(distribution):
    """
    Returns the lists of high and low probability rolls
    """
    high_probability_rolls = np.argwhere(np.max(distribution) == distribution).reshape(1, -1)
    high = high_probability_rolls.tolist()[0]
    low = [roll for roll in list(range(2, 13)) if roll not in high]
    return high, low


if __name__ == '__main__':
    d = np.array([0, 0, .1, .1, .4, .4, 0, 0, 0, 0, 0, 0, 0])
    h, lo = high_low_rolls(d)
    print(h, lo)
