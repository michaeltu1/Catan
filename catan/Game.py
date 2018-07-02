class Game:
    def __init__(self):
        self.intersections = None
        self.unbuildable = set()
        
        resource_cards = {"Wheat" : 19, "Sheep" : 19, "Ore" : 19, "Clay" : 19, "Wood" : 19}
        dev_cards = {"Knight" : 14, "Victory Point" : 5, "Road Building" : 2, "Year of Plenty" : 2, "Monopoly" : 2}

        self.game_resources = Inventory(resource_cards, dev_cards)

    """
    Take in a player_id and attempt to build a road at an edge tuple (x, y)
    returns true if successful, otherwise false.
    """
    def build_road(self, player_id, edge):
        if edge.has_road is False:
            edge.has_road = True
            # check longest road
            return True
        return False

    """
    Take in a player_id and attempt to build a settlement at an intersection tuple (x, y, z)
    returns true if successful, otherwise false.
    
    Start with an empty set in Game, then add intersections to the 
        set if you can no longer build on that intersection.
    """
    def build_settlement(self, player_id, intersection):
        if intersection not in Game.unbuildable:
            Game.unbuildable.add(intersection)
            Game.unbuildable.add((intersection.index(0) + 20,
                                  intersection.index(1), intersection.index(2)))
            Game.unbuildable.add((intersection.index(0),
                                  intersection.index(1) - 7, intersection.index(2)))
            Game.unbuildable.add((intersection.index(0),
                                  intersection.index(1), intersection.index(2) - 13))
            intersection.has_settlement = True
            # check longest road
            return True
        return False

    """
    Take in a player_id and attempt to build a city at an intersection tuple (x, y, z)
    returns true if successful, otherwise false.
    """
    def build_city(self, player_id, intersection):
        if intersection.has_settlement is True:
            intersection.has_city = True
            intersection.has_settlement = False
            return True
        return False

    """
    Take in a player_id and attempt to buy a dev card
    returns true if successful and will add the dev card to player's backpack, otherwise returns false
    """
    def buy_dev_card(self, player_id):
        return False

    """
    Take in a player_id and two resource types;
    By default it's a 4:1 trade from resource_1 -> resource_2
    if other_player_id is positive then attempt to trade with other player
    else if port_name is not None: do a trade according to the port type and resource_1 and resource_2
    returns True if trade was successful, otherwise prints out what went wrong and returns false.
    """
    def trade(self, player_id, resource_1, resource_2, other_player_id=0, port_name=None):
        return True


