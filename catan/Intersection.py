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

    """
    Start with an empty set in Game, then add intersections to the 
        set if you can no longer build on that intersection.
    """
    def build(self):
        # if not (self.has_city or self.has_settlement):
        #     for intersection in Board.intersections:
        #
        #         return True
        if self.intersect_ID not in Game.unbuildable:
            Game.unbuildable.add(self.intersect_ID)
            Game.unbuildable.add((self.intersect_ID.index(0) + 20,
                                  self.intersect_ID.index(1), self.intersect_ID.index(2)))
            Game.unbuildable.add((self.intersect_ID.index(0),
                                  self.intersect_ID.index(1) - 7, self.intersect_ID.index(2)))
            Game.unbuildable.add((self.intersect_ID.index(0),
                                  self.intersect_ID.index(1), self.intersect_ID.index(2) - 13))
