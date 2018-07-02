import numpy as np
from catan.Player import *

class Game:
    def __init__(self):
        self.intersections = None
        self.unbuildable = set()
        
        resource_cards = {"Wheat" : 19, "Sheep" : 19, "Ore" : 19, "Clay" : 19, "Wood" : 19}
        dev_cards = {"Knight" : 14, "Victory Point" : 5, "Road Building" : 2, "Year of Plenty" : 2, "Monopoly" : 2}

        self.game_resources = Inventory(resource_cards, dev_cards)


    def start_game(self, num_players):
        self.player_list = []
        max_roll = (0, 0)   # (player_id, roll_num)

        # Create players, player_id starts at 1 and decide who goes first, todo: tie breaker?
        for number in range(num_players):
            player = Player(number)
            r = roll_dice()
            max_roll = (number, r) if r > max_roll[1] else max_roll
            self.player_list.append(player) 
        
        for player_id in range(max_roll[0], max_roll[0] + num_players):
            player_id %= (num_players + 1)
            # response = where would you like to build? check if possible
            build_settlement(player_id, response)
            build_road(player_id, response)

#b = game.player_list[0].backpack
#print(b), can't print out actual information for some reason

"""
Returns the sum of two dice rolls
"""
def roll_dice():
    rolls = np.random.choice([1, 2, 3, 4, 5, 6], 2)
    return rolls[0] + rolls[1]

"""
Given a player and roll_num, distribute resources according to what tiles the player owns
"""
def distribute_resources(player_id, roll_num):
    

"""
Take in a player_id and attempt to build a road at an edge tuple (x, y)
returns true if successful, otherwise false.
"""
def build_road(player_id, edge):
    return False

"""
Take in a player_id and attempt to build a settlement at an intersection tuple (x, y, z)
returns true if successful, otherwise false.
"""
def build_settlement(player_id, intersection):
    return False

# originally in intersection but moved to here
# need to update board or game with updated intersection attributes (has_settlement or has_city)
def build_settlement():
    if self.intersect_ID not in Game.unbuildable:
        Game.unbuildable.add(self.intersect_ID)
        Game.unbuildable.add((self.intersect_ID.index(0) + 20, self.intersect_ID.index(1), self.intersect_ID.index(2)))
        Game.unbuildable.add((self.intersect_ID.index(0), self.intersect_ID.index(1) - 7, self.intersect_ID.index(2)))
        Game.unbuildable.add((self.intersect_ID.index(0), self.intersect_ID.index(1), self.intersect_ID.index(2) - 13))

"""
Take in a player_id and attempt to build a city at an intersection tuple (x, y, z)
returns true if successful, otherwise false.
"""

def build_city(player_id, intersection):
    return False


"""
Take in a player_id and attempt to buy a dev card
returns true if successful and will add the dev card to player's backpack, otherwise returns false
"""
def buy_dev_card(player_id):
    return False

"""
Take in a player_id and two resource types;
By default it's a 4:1 trade from resource_1 -> resource_2
if other_player_id is positive then attempt to trade with other player
else if port_name is not None: do a trade according to the port type and resource_1 and resource_2
returns True if trade was successful, otherwise prints out what went wrong and returns false.
"""
def trade(player_id, resource_1, resource_2, other_player_id=-1, port_name=None):
    return True


