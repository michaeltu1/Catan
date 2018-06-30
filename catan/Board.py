import random

# TODO(mtu): figure out how imports work
from catan.config.Config import Config
from catan.Tile import Tile
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

        self.land_tile_ids = [18, 20, 22,
                              7, 9, 11, 13,
                              -4, -2, 0, 2, 4,
                              -13, -11, -9, -7,
                              -22, -20, -18]
        self.ocean_tile_ids = [1033, 1035, 1037, 1039,
                               1022, 1026,
                               1011, 1016,
                               1000, 1006,
                               991, 1001,
                               982, 990,
                               973, 975, 977, 979]
        self.collectible_resource_types = ["Wheat"] * 4 + ["Sheep"] * 4 + ["Ore"] * 3 + ["Clay"] * 3 + ["Wood"] * 4

        self.port_types = ["Sheep", "Clay", "Wood", "Wheat", "Ore"] + ["3:1"] * 4

        self.roll_nums = [2] + [3, 4, 5, 6, 8, 9, 10, 11] * 2 + [12]

    def generate_random_board(self):
        # TODO(mtu): enforce dice invariants
        # TODO(mtu): assign ports
        random.shuffle(self.land_tile_ids)
        random.shuffle(self.collectible_resource_types)
        random.shuffle(self.port_types)
        random.shuffle(self.roll_nums)

        tile_configs = []

        # Save the last tile to be assigned as the desert
        for tile_id, resource, roll_num in self.land_tile_ids[:-1], self.collectible_resource_types, self.roll_nums:
            tile_configs.append([tile_id, resource, roll_num, set(), set()])

        # Create the land tile -- the desert tile
        tile_configs.append([tile_id, resource, roll_num, set(), set(), True])

        # Create all ocean tiles
        for tile_id in self.ocean_tile_ids:
            tile_configs.append([tile_id, "Ocean", -1, set(), set()])

        tile_objects = []
        for config in tile_configs:
            tile_objects.append(Tile(*config))

        return tile_objects

    def __str__(self):
        # TODO(mtu): print the board
        return "blah"


if __name__ == '__main__':
    b = Board()
    print(b)
