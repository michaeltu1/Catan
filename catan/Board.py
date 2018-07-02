import random

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

        self.land_tile_ids = [18, 20, 22,
                              7, 9, 11, 13,
                              -4, -2, 0, 2, 4,
                              -13, -11, -9, -7,
                              -22, -20, -18]
        self.ocean_tile_ids = [27, 29, 31, 33,
                               16, 24,
                               5, 15,
                               -6, 6,
                               -15, -5,
                               -24, -16,
                               -33, -31, -29, -27]
        self.collectible_resource_types = ["Wheat"] * 4 + ["Sheep"] * 4 + ["Ore"] * 3 + ["Clay"] * 3 + ["Wood"] * 4

        self.port_types = ["Sheep", "Clay", "Wood", "Wheat", "Ore"] + ["3:1"] * 4

        self.roll_nums = [2] + [3, 4, 5, 6, 8, 9, 10, 11] * 2 + [12]

    def create_roll_num_assignment(self):
        """
        After the function is completed, we are guaranteed that high probability roll numbers
        are not placed on tiles adjacent to each other
        """
        # Retrieve high and low probability dice roll numbers
        common_rolls, uncommon_rolls = high_low_rolls(self.distribution)

        # Keys are the index of the land_tile_ids
        # Values are the indices of land_tile_ids adjacent to the land_tile corresponding to the key
        adj = {0: {1, 3, 4},
               1: {0, 2, 4, 5},
               2: {1, 5, 6},
               3: {0, 4, 7, 8},
               4: {0, 1, 3, 5, 8, 9},
               5: {1, 2, 4, 6, 9, 10},
               6: {2, 5, 10, 11},
               7: {3, 8, 12},
               8: {3, 4, 7, 9, 12, 13},
               9: {4, 5, 8, 10, 13, 14},
               10: {5, 6, 9, 11, 14, 15},
               11: {6, 10, 15},
               12: {7, 8, 13, 16},
               13: {8, 9, 12, 14, 16, 17},
               14: {9, 10, 13, 15, 17, 18},
               15: {10, 11, 14, 18},
               16: {12, 13, 17},
               17: {13, 14, 16, 18},
               18: {14, 15, 17}}

        valid_assignment = False
        while not valid_assignment:
            # Repeatedly randomly shuffle until a valid_assignment of roll_nums is generated
            random.shuffle(self.roll_nums)

            # Find the indices of the land_tile_ids that will have the high probability dice rolls
            common_roll_locations = [index for index, roll_num in enumerate(self.roll_nums) if roll_num in common_rolls]

            location_checks = [True]
            for i in range(len(common_roll_locations)):
                current_location = common_roll_locations[i]
                other_locations = common_roll_locations[i + 1:]
                location_checks.append(all([True if o in adj[current_location] else False for o in other_locations]))

            valid_assignment = all(location_checks)

    def generate_random_board(self):
        # TODO(mtu): assign ports to intersection
        # TODO(mtu): construct edges, intersections, and tiles
        random.shuffle(self.collectible_resource_types)
        random.shuffle(self.port_types)
        self.create_roll_num_assignment()

        tile_configs = []

        # Design all land tile configurations except for the desert tile
        for tile_id, resource, roll_num in self.land_tile_ids[:-1], self.collectible_resource_types, self.roll_nums:
            tile_configs.append([tile_id, resource, roll_num])

        # Design desert tile configuration
        tile_configs.append([tile_id, resource, roll_num, True])

        # Design all ocean tile configs
        for tile_id in self.ocean_tile_ids:
            tile_configs.append([tile_id, "Ocean", 0])

        # Instantiate all tiles with given config
        tile_objects = []
        for config in tile_configs:
            tile_objects.append(Tile(*config))

        # Construct all edges here
        edge_ids = [(18, 27), (18, 29), (20, 29), (20, 31), (22, 31), (22, 33),
                    (16, 18), (18, 20), (20, 22), (22, 24),
                    (7, 16), (7, 18), (9, 18), (9, 20), (11, 20), (11, 22), (13, 22), (13, 24),
                    (5, 7), (7, 9), (9, 11), (11, 13), (13, 15),
                    (-4, 5), (-4, 7), (-2, 7), (-2, 9), (0, 9), (0, 11), (2, 11), (2, 13), (4, 13), (4, 15),
                    (-6, -4), (-4, -2), (-2, 0), (0, 2), (2, 4), (4, 6),
                    (-15, -4), (-13, -4), (-13, -2), (-11, -2), (-11, 0), (-9, 0), (-9, 2), (-7, 2), (-7, 4), (-5, 4),
                    (-15, -13), (-13, -11), (-11, -9), (-9, -7), (-7, -5),
                    (-24, -13), (-22, -13), (-22, -11),(-20, -11), (-20, -9), (-18, -9), (-18, -7), (-16, -7),
                    (-24, -22), (-22, -20), (-20, -18), (-18, -16),
                    (-33, -22), (-31, -22), (-31, -20), (-29, -20), (-29, -18), (-27, -18)]

        edge_objects = [Edge(*config) for config in edge_configs]

        # Construct all intersections here -- some have ports!!
        intersection_ids = [(, , ), (, , ), (, , ), (, , ), (, , ), (, , ), (, , ), (, , ), (, , ), (, , ), (, , ), (, , ),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),
                            (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,), (, ,),]

        return tile_objects

    def __str__(self):
        # TODO(mtu): print the board
        return "blah"


if __name__ == '__main__':
    b = Board()
    print(b)
