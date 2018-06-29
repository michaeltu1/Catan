# TODO(mtu): figure out how imports work
from catan.config.Config import Config
from catan.Utils import *


class Board:

    def __init__(self, mode="standard"):
        """
        :param mode: determines the configuration of the game
        """
        c = Config()
        # Initialize game rules
        self.config = c.get_config(mode)

        # Get the sampling distribution of the dice
        # Distribution is a normalized numpy array
        dice = self.config["dice"]
        self.distribution = c.get_normalized_distribution(dice)

        # Retrieve high and low probability dice roll numbers
        common_rolls, uncommon_rolls = high_low_rolls(self.distribution)

    def __str__(self):
        # TODO(mtu): print the board
        raise NotImplementedError


if __name__ == '__main__':
    b = Board()
    print(b)
