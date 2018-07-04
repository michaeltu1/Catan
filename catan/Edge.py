class Edge:

    """
    Edge ID will be represented as a tuple consisting of adjacent tiles' IDs.
    By default, no edges will have roads on them.
    """

    def __init__(self, tile_1, tile_2):
        self.edge_ID = (tile_1, tile_2)
        self.has_road = False

    def build_road(self, edge_id):
        if "???".has_road is False:
            # TODO: somehow reach edge object from intersect ID
            "???".has_road = True
            # check longest road

    # TODO: Implement BFS in Python to determine longest road when road/settlement is placed.

    def check_longest_road(self):
        return self.has_road

    def __str__(self):
        return "Edge id: %s, has road: %s" % (self.edge_ID, self.has_road)

    def __repr__(self):
        return str(self)


if __name__ == '__main__':
    test_edge = Edge(50, 20)
    print(test_edge.edge_ID)
