class Inventory:
    """
    Game.py should initialize the dictionary of resource and dev cards
    should map resource type (key) to number of that type of card (value), 
    also initialize ports
    and initialize longest_road and largest_army to true;
    a player by default has no cards and no ports

    TODO: Figure out how to represents ports, location of port comes from intersection,
    but need to also know what type of port and quantity.
    """
    def __init__(self, resource_cards={}, dev_cards={}, ports=set(), longest_road=False, largest_army=False):
        self.resource_cards = resource_cards
        self.dev_cards = dev_cards
        self.ports = ports
        self.longest_road = longest_road
        self.largest_army = largest_army


class Backpack(Inventory):
    """
    Each Player has a backpack that keeps track of all the player's possessions
    cities and settlements should be a set of intersection tuples
    roads should be a set of edge ids (tentative, since we don't know how two edges connect)
    """
    def __init__(self, cities=set(), settlements=set(), roads=set()):
        Inventory.__init__(self)
        self.cities = cities
        self.settlements = settlements
        self.roads = roads
