class Edge:

    """
    Edge ID will be determined by the average of the adjacent tiles' IDs.
    By default, no edges will have roads on them.
    """

    def __init__(self, tile_1, tile_2):
        self.edge_ID = (tile_1 + tile_2)/2
        self.has_road = False

    def id(self):
        return self.edge_ID

    # Todo: Implement BFS in Python to determine longest road

if __name__ == '__main__':
    test_edge = Edge(50, 20)
    print(test_edge.edge_ID)
