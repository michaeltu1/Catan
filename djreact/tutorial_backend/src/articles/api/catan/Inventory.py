class Inventory:
    """
    Game.py should initialize the dictionary of resource and dev cards
    should map resource type (key) to number of that type of card (value),
    a player's dev_card will map "type" to DevCard Class
    also initialize ports

    a player by default has no cards and no ports

    """
    def __init__(self, resource_cards=None, dev_cards=None):
        self.resource_cards = resource_cards or {}
        self.dev_cards = dev_cards or []

    def __str__(self):
        return "Resource cards: %s, Dev cards: %s" % (self.resource_cards, self.dev_cards)

    def __repr__(self):
        dev_card_str = [dc.__repr__() for dc in self.dev_cards]
        return "Inventory(%s, %s)" % (self.resource_cards, dev_card_str)


class Backpack(Inventory):
    """
    Each Player has a backpack that keeps track of all the player's possessions;
        better way to combine rolls and tiles into one?
    Rolls dictionary maps dice_roll to set of tile_ids 
    Tile dictionary maps tile_id to number of resource collected
    roads should be a set of edge tuples
    """
    def __init__(self, num_settlements, num_cities, num_roads, num_cards=0, victory_points=0,
                 rolls=None, tiles=None, settlements=None, roads=None, ports=None):
        Inventory.__init__(self)
        self.num_settlements = num_settlements
        self.num_cities = num_cities
        self.num_roads = num_roads
        self.num_cards = num_cards
        self.victory_points = victory_points
        self.rolls = rolls or {}
        self.tiles = tiles or {}
        self.settlements = settlements or set()
        self.roads = roads or set()
        self.ports = ports or set()

    def __str__(self):
        return "resource cards: %s, dev_cards: %s, settlements: %s, cities: %s, roads: %s, cards: %s, " \
               "victory points: %s, rolls: %s, tiles: %s, settlements: %s, roads: %s, ports: %s" % \
                (self.resource_cards, self.dev_cards, self.num_settlements, self.num_cities, self.num_roads,
                 self.num_cards, self.victory_points, self.rolls, self.tiles, self.settlements, self.roads, self.ports)

    def __repr__(self):
        return "Backpack(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" % \
                (self.resource_cards, self.dev_cards, self.num_settlements, self.num_cities, self.num_roads,
                 self.num_cards, self.victory_points, self.rolls, self.tiles, self.settlements, self.roads, self.ports)
