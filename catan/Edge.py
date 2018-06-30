class Edge:

    """
    Edge ID will be represented as a tuple consisting of adjacent tiles' IDs.
    By default, no edges will have roads on them.
    """

    def __init__(self, tile_1, tile_2):
        self.edge_ID = (tile_1, tile_2)
        self.has_road = False

    # TODO: Implement BFS in Python to determine longest road
    def build_road(self):
        self.has_road = True


if __name__ == '__main__':
    test_edge = Edge(50, 20)
    print(test_edge.edge_ID)
