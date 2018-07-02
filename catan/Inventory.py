class Inventory:
    """
    Game.py should initialize the dictionary of resource and dev cards
    should map resource type (key) to number of that type of card (value), 
    also initialize ports

    Move longest road /largest_army to game.py and have it keep track of player id
    a player by default has no cards and no ports

    """
    def __init__(self, resource_cards={}, dev_cards={}):
        self.resource_cards = resource_cards
        self.dev_cards = dev_cards

    def __str__(self):
        return "resource cards: %s, dev cards %s" % (self.resource_cards, self.dev_cards)

    def __repr__(self):
        return str(self)


class Backpack(Inventory):
    """
    Each Player has a backpack that keeps track of all the player's possessions;
    Tile dictionary maps tile_id to number of resource collected
    roads should be a set of edge tuples
    """
    def __init__(self, num_settlements, num_cities, num_roads, victory_points=0, tiles={}, roads=set(), ports=set()):
        Inventory.__init__(self)
        self.num_settlements = num_settlements
        self.num_cities = num_cities
        self.num_roads = num_roads
        self.victory_points = victory_points
        self.tiles = tiles
        self.roads = roads
        self.ports = ports

    def __str__(self):
        return "settlements: %s, cities: %s, roads: %s, victory points: %s, tiles: %s, roads: %s, ports: %s" % \
                (self.num_settlements, self.num_cities, self.num_roads, self.victory_points, self.tiles, \
                 self.roads, self.ports)

    def __repr__(self):
        return str(self)

#ex_backpack = Backpack(5, 4, 15)
