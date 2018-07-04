class Intersection:

    """
    Intersections will be referenced as tuples of the 3 adjacent tiles' IDs.
    Ports will exist at some of the intersections between resource and ocean tiles;
        their placement to be determined by game.py.
    By default, no intersections will not have settlements or cities on them.
    """

    def __init__(self, tile_1, tile_2, tile_3, port=None):
        self.intersect_ID = (tile_1, tile_2, tile_3)
        self.port = port
        self.has_settlement = False
        self.has_city = False

    def __str__(self):
        return "Intersection id: %s, port: %s, has settlement: %s, has city: %s" \
               % (self.intersect_ID, self.port, self.has_settlement, self.has_city)

    def __repr__(self):
        return str(self)


    # def build_settlement(self, intersect_id):
    #     if intersect_id not in Game.unbuildable:
    #         Game.unbuildable.add(intersect_id)
    #         Game.unbuildable.add((intersect_id.index(0) + 20,
    #                               intersect_id.index(1), intersect_id.index(2)))
    #         Game.unbuildable.add((intersect_id.index(0),
    #                               intersect_id.index(1) - 7, intersect_id.index(2)))
    #         Game.unbuildable.add((intersect_id.index(0),
    #                               intersect_id.index(1), intersect_id.index(2) - 13))
    #         # TODO: somehow reach intersection object from intersect ID
    #         "???".has_settlement = True
    #         # check longest road
