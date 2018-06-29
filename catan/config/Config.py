import numpy as np


class Config:

    def __init__(self):
        self.config = {"standard": {"dice": "fair",
                                    "board": "random"},
                       }

        # TODO: Possibly allow customization of the number of dice and frequency of each roll
        # The value of each entry in the array represents the frequency of each dice roll
        self.distributions = {"fair": np.array([0, 0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1]),
                              "inverted": np.array([0, 0, 6, 5, 4, 3, 2, 1, 2, 3, 4, 5, 6])}

    def get_config(self, mode="standard"):
        return self.config[mode]

    def get_normalized_distribution(self, mode="fair"):
        distribution = self.distributions[mode]
        total = np.sum(distribution)
        return distribution / total
