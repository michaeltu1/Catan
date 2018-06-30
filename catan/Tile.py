class Tile:
    # Intersections keeps track of a set of tuples that are the keys 
    # to the intersection dictionary

    # Edges keeps track of a set of unique ids that are the keys
    # to the edges dictionary

    def __init__(self, tile_id, resource_type, roll_num, edges, intersections, has_robber=False):
        self.tile_id = tile_id
        self.resource_type = resource_type
        self.roll_num = roll_num
        self.edges = edges
        self.intersections = intersections
        self.has_robber = has_robber
    
    def adjacent_tile(self, tile_other):
        for edge in self.edges:
            if edge in tile_other.edges:
                return True
        return False

    def __str__(self):
        # print the attributes of this tile
        return "Tile id: %s, roll num: %s, resource: %s" % (self.tile_id, self.roll_num, self.resource_type) 


#e = set()
#i = set()
#example_tile = Tile(0, "Wheat", 6, e, i)
#example_tile2 = Tile(1, "Desert", 7, e, i, True)
