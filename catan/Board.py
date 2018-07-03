import random

from catan.config.Config import Config
from catan.Tile import Tile
from catan.Edge import Edge
from catan.Intersection import Intersection
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
        self.land_tile_objects = [0] * 19
        self.tile_objects, self.edge_objects, self.intersection_objects = self.generate_random_board()

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

            # Check at all points with high frequency rolls that it is not next to another high frequency roll
            location_checks = [True]
            for i in range(len(common_roll_locations)):
                current_location = common_roll_locations[i]
                other_locations = common_roll_locations[i + 1:]
                location_checks.extend([False if o in adj[current_location] else True for o in other_locations])

            valid_assignment = all(location_checks)

    def generate_random_board(self):
        # Randomize resource and port locations
        random.shuffle(self.collectible_resource_types)
        random.shuffle(self.port_types)

        # Generate a valid, random dice roll arrangement
        self.create_roll_num_assignment()

        # List of tile configs used to instantiate tiles
        tile_configs = []

        # Randomize order of tile_id assignment
        tile_ids = self.land_tile_ids.copy()
        random.shuffle(tile_ids)

        # Design all land tile configurations except for the desert tile
        for i in range(18):
            tile_configs.append([tile_ids[i], self.collectible_resource_types[i], [self.roll_nums[i]]])

        # Design desert tile configuration
        tile_configs.append([tile_ids[-1], "Desert", 0, True])
        self.land_tile_objects = [Tile(*config) for config in tile_configs]

        # Design all ocean tile configs
        for tile_id in self.ocean_tile_ids:
            tile_configs.append([tile_id, "Ocean", 0])

        # Instantiate all tiles with given config
        tile_objects = [Tile(*config) for config in tile_configs]

        # List of edge_ids used to construct edges
        edge_ids = [(18, 27), (18, 29), (20, 29), (20, 31), (22, 31), (22, 33),
                    (16, 18), (18, 20), (20, 22), (22, 24),
                    (7, 16), (7, 18), (9, 18), (9, 20), (11, 20), (11, 22), (13, 22), (13, 24),
                    (5, 7), (7, 9), (9, 11), (11, 13), (13, 15),
                    (-4, 5), (-4, 7), (-2, 7), (-2, 9), (0, 9), (0, 11), (2, 11), (2, 13), (4, 13), (4, 15),
                    (-6, -4), (-4, -2), (-2, 0), (0, 2), (2, 4), (4, 6),
                    (-15, -4), (-13, -4), (-13, -2), (-11, -2), (-11, 0), (-9, 0), (-9, 2), (-7, 2), (-7, 4), (-5, 4),
                    (-15, -13), (-13, -11), (-11, -9), (-9, -7), (-7, -5),
                    (-24, -13), (-22, -13), (-22, -11), (-20, -11), (-20, -9), (-18, -9), (-18, -7), (-16, -7),
                    (-24, -22), (-22, -20), (-20, -18), (-18, -16),
                    (-33, -22), (-31, -22), (-31, -20), (-29, -20), (-29, -18), (-27, -18)]

        edge_objects = [Edge(*edge_id) for edge_id in edge_ids]

        # List of intersection ids with ports (every 2 consecutive ids have the same port type)
        port_intersections = [[-31, -22, -20], [-31, -29, -20], [-29, -27, -18], [-27, -18, -16],
                              [-24, -15, -13], [-24, -22, -13], [-16, -7, -5], [-7, -5, 4],
                              [-15, -6, -4], [-6, -4, 5],
                              [4, 13, 15], [13, 15, 24],
                              [7, 16, 18], [16, 18, 27],
                              [18, 20, 29], [20, 29, 31], [22, 31, 33], [22, 24, 33]]

        # List of intersection ids without ports
        non_port_intersections = [(-33, -24, -22), (-33, -31, -22),
                                  (-22, -13, -11),
                                  (-22, -20, -11), (-20, -11, -9), (-20, -18, -9), (-18, -9, -7), (-18, -16, -7),
                                  (-15, -13, -4), (-13, -4, -2), (-13, -11, -2), (-11, -2, 0),
                                  (-11, -9, 0), (-9, 0, 2), (-9, -7, 2), (-7, 2, 4), (-5, 4, 6),
                                  (-4, 5, 7), (-4, -2, 7), (-2, 7, 9), (-2, 0, 9), (0, 9, 11), (0, 2, 11), (2, 11, 13),
                                  (2, 4, 13), (4, 6, 15), (5, 7, 16), (7, 9, 18), (9, 18, 20),
                                  (9, 11, 20), (11, 20, 22), (11, 13, 22), (13, 22, 24),
                                  (18, 27, 29), (20, 22, 31)]

        for i in range(0, len(port_intersections), 2):
            port = self.port_types[i // 2]
            port_intersections[i].append(port)
            port_intersections[i + 1].append(port)
        port_intersection_objects = [Intersection(*config) for config in port_intersections]

        non_port_intersection_objects = [Intersection(*intersection_id) for intersection_id in non_port_intersections]

        return tile_objects, edge_objects, non_port_intersection_objects + port_intersection_objects

    def __str__(self):
        # Print out board tiles -- for each tile show (roll_num, resource)
        to_print = [0] * 19
        for t in self.land_tile_objects:
            to_print[self.land_tile_ids.index(t.tile_id)] = (t.resource_type + " " + str(t.roll_num))

        port_printable = [io.port for io in self.intersection_objects[-18:]]

        return "\n                    {:<20}{:<20}{:<20}\n\n" \
               "          {:<20}{:<20}{:<20}{:<20}\n\n" \
               "{:<20}{:<20}{:<20}{:<20}{:<20}\n\n" \
               "          {:<20}{:<20}{:<20}{:<20}\n\n" \
               "                    {:<20}{:<20}{:<20}\n".format(*to_print) + "\n" + str(port_printable)


if __name__ == '__main__':
    b = Board()
    print(b)
