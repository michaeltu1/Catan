class Tile:
    """
    Intersections keeps track of a set of tuples that are the keys 
    to the intersection dictionary

    Edges keeps track of a set of unique ids that are the keys
    to the edges dictionary

    adjacent_tile returns whether a given tile is adjacent to the current tile
    """

    def __init__(self, tile_id, resource_type, roll_num, has_robber=False):
        self.tile_id = tile_id
        self.resource_type = resource_type
        self.roll_num = roll_num
        self.has_robber = has_robber
    
    def adjacent_tile(self, tile_other):
        other_id = tile_other.tile_id
        my_id = self.tile_id
        return my_id + 2 == other_id or my_id + 9 == other_id or my_id + 11 == other_id or \
               my_id - 2 == other_id or my_id - 9 == other_id or my_id - 11 == other_id

    def __str__(self):
        # print the attributes of this tile
        return "Tile id: %s, roll num: %s, resource: %s" % (self.tile_id, self.roll_num, self.resource_type) 

    def __repr__(self):
        return str(self)


#e = set()
#i = set()
#example_tile = Tile(0, "Wheat", 6, e, i)
#example_tile2 = Tile(1, "Desert", 7, e, i, True)
