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

    def adjacent_edges(self):
        edges = set()
        edges.add((self.intersect_ID[0], self.intersect_ID[1]))
        edges.add((self.intersect_ID[1], self.intersect_ID[2]))
        edges.add((self.intersect_ID[0], self.intersect_ID[2]))
        return edges


    def __str__(self):
        return "Intersection id: %s, port: %s, has settlement: %s, has city: %s" \
               % (self.intersect_ID, self.port, self.has_settlement, self.has_city)

    def __repr__(self):
        return str(self)
