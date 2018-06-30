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

    # TODO: needs to check that adjacent intersections do not contain buildings.
    def can_build(self):
        if not (self.has_city or self.has_settlement):
            for intersection in Game.intersections:

                return True