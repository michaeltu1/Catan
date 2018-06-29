import random

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

        self.tile_ids = [x for x in range(19)]
        self.resource_types = ["Wheat"] * 4 + ["Sheep"] * 4 + ["Ore"] * 3 + \
                              ["Clay"] * 3 + ["Wood"] * 4 + ["Desert"]

    """
    def generate_random_board(self):
        random.shuffle(self.tile_ids)
        random.shuffle(resource_types)
        zip(self.tile_ids, self.resource_types)
    """

    def __str__(self):
        # TODO(mtu): print the board
        return "blah"


if __name__ == '__main__':
    b = Board()
    print(b)
