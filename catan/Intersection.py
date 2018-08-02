class Intersection:

    """
    Intersections will be referenced as tuples of the 3 adjacent tiles' IDs.
    Ports will exist at some of the intersections between resource and ocean tiles;
        their placement to be determined by game.py.
    By default, no intersections will not have settlements or cities on them.
    """

    def __init__(self, intersect_id, port=None, has_settlement=False, has_city=False):
        self.intersect_ID = intersect_id
        self.port = port
        self.has_settlement = has_settlement
        self.has_city = has_city

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
        return "Intersection(%s, %s, %s, %s)" \
               % (self.intersect_ID, self.port, self.has_settlement, self.has_city)
