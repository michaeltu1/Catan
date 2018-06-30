from catan.Game import *


class Intersection:

    """
    Intersections will be referenced as tuples of the 3 adjacent tiles' IDs.
    Ports will exist at some of the intersections between resource and ocean tiles;
        their placement to be determined by game.py.
    By default, no intersections will not have settlements or cities on them.
    """

    def __init__(self, tile_1, tile_2, tile_3):
        self.intersect_ID = (tile_1, tile_2, tile_3)
        self.has_port = False
        self.has_settlement = False
        self.has_city = False

    # TODO: need to update set of intersections on which we can build.
    # Start with an empty set, then add intersections to the set if you cannot build an intersection on that spot
    def build(self):
        # if not (self.has_city or self.has_settlement):
        #     for intersection in Board.intersections:
        #
        #         return True
        if self.intersect_ID not in Game.unbuildable:
            Game.unbuildable.add(self.intersect_ID)
            Game.unbuildable.add((self.intersect_ID.index(0), self.intersect_ID.index(1), top_tile_ID))
            Game.unbuildable.add((self.intersect_ID.index(1), self.intersect_ID.index(2), bottomleft_tile_ID))
            Game.unbuildable.add((self.intersect_ID.index(0), self.intersect_ID.index(2), bottomright_tile_ID))
