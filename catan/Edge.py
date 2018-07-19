class Edge:

    """
    Edge ID will be represented as a tuple consisting of adjacent tiles' IDs.
    By default, no edges will have roads on them.
    """

    def __init__(self, tile_1, tile_2):
        self.edge_ID = (tile_1, tile_2)
        self.has_road = False

    """
    Return whether or not another is edge is adjacent to this one 
    """
    def adjacent_edge(self, other):
        sum1 = self.edge_ID[0] + self.edge_ID[1]
        sum2 = other.edge_ID[0] + other.edge_ID[1]
        result = abs(sum2 - sum1)
        return result == 2 or result == 9 or result == 11

    def get_vertices(self):
        vertices = set()
        diff = self.edge_ID[1] - self.edge_ID[0]
        if diff == 2:
            vertices.add((self.edge_ID[0] - 9, self.edge_ID[0], self.edge_ID[1]))
            vertices.add((self.edge_ID[0], self.edge_ID[1], self.edge_ID[1] + 9))
        elif diff == 9:
            vertices.add((self.edge_ID[0], self.edge_ID[1], self.edge_ID[1] + 2))
            vertices.add((self.edge_ID[0] - 2, self.edge_ID[0], self.edge_ID[1]))
        elif diff == 11:
            vertices.add((self.edge_ID[0], self.edge_ID[1] - 2, self.edge_ID[1]))
            vertices.add((self.edge_ID[0], self.edge_ID[0] + 2, self.edge_ID[1]))
        return vertices
    
    def check_longest_road(self):
        return self.has_road

    def __str__(self):
        return "Edge id: %s, has road: %s" % (self.edge_ID, self.has_road)

    def __repr__(self):
        return str(self)
