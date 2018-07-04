import numpy as np
from catan.Player import *

class Game:
    def __init__(self):
        self.intersections = None
        self.unbuildable = set()
        
        resource_cards = {"Wheat" : 19, "Sheep" : 19, "Ore" : 19, "Clay" : 19, "Wood" : 19}
        dev_cards = {"Knight" : 14, "Victory Point" : 5, "Road Building" : 2, "Year of Plenty" : 2, "Monopoly" : 2}

        self.game_resources = Inventory(resource_cards, dev_cards)
        self.game_over = False


    def start_game(self, num_players):
        self.player_list = []
        player_ids = []

        # Create players, player_id starts at 1 
        for number in range(num_players):
            player = Player(number)
            self.player_list.append(player) 
            player_ids.append(number)
        
        # Decide who goes first
        player_first = _starter(player_ids)

        
        # First round of choosing settlements and roads
        for player_id in range(player_first, player_first + num_players):
            player_id %= num_players
            _ux(player_id, "build settlement")
            _ux(player_id, "build road")

        # Second round of choosing settlements and roads
        for player_id in reversed(range(player_first, player_first + num_players)):
            player_id %= num_players
            _ux(player_id, "build settlement")

            # Get the rolls num associated with the tiles that the settlement are touching
            # and give those resources to the player
            for roll_num in self.player_list[player_id].backpack.rolls.keys():
                distribute_resources(player_id, roll_num)
            _ux(player_id, "build road")
        
        while not self.game_over:
            for player_id in range(player_first, player_first + num_players):
                r = roll_dice()
                distribute_resources(player_id, r)

                done = False
                while not done:
                    action = _ux(player_id, "ask for action")
                    done = _ux(player_id, action)

                if self.player_list[player_id].backpack.victory_points == 10:
                    self.game_over = True
                    print("Player %s has won the game" % player_id)

    """
    Given a player and roll_num, distribute resources according to what tiles the player owns
    """
    def distribute_resources(self, player_id, roll_num):
        

    """
    Take in a player_id and attempt to build a road at an edge tuple (x, y)
    Need to update player's backpack's num_roads, roads
    returns true if successful, otherwise false.
    """
    def build_road(self, player_id, edge):
        return False

    """
    Take in a player_id and attempt to build a settlement at an intersection tuple (x, y, z)
    Need to update player's backpack's num_settlements, victory_points, rolls, tiles, and ports if applicable
    returns true if successful, otherwise false.

    originally in intersection but moved to here
    need to update board or game with updated intersection attributes (has_settlement or has_city)
    """
    def build_settlement(self, player_id, intersection):
        if self.intersect_ID not in Game.unbuildable:
            Game.unbuildable.add(self.intersect_ID)
            Game.unbuildable.add((self.intersect_ID.index(0) + 20, self.intersect_ID.index(1), self.intersect_ID.index(2)))
            Game.unbuildable.add((self.intersect_ID.index(0), self.intersect_ID.index(1) - 7, self.intersect_ID.index(2)))
            Game.unbuildable.add((self.intersect_ID.index(0), self.intersect_ID.index(1), self.intersect_ID.index(2) - 13))
        return False

    """
    Take in a player_id and attempt to build a city at an intersection tuple (x, y, z)
    returns true if successful, otherwise false.
    """

    def build_city(self, player_id, intersection):
        return False


    """
    Take in a player_id and attempt to buy a dev card
    returns true if successful and will add the dev card to player's backpack, otherwise returns false
    """
    def buy_dev_card(self, player_id):
        return False

    """
    Take in a player_id and use a dev card
    make sure that the card wasn't bought in the same turn
    returns true if used successfully, otherwise returns false
    """

    def use_dev_card(self, player_id):
        return False


    """
    Take in a player_id and two resource types;
    By default it's a 4:1 trade from resource_1 -> resource_2
    if other_player_id is positive then attempt to trade with other player
    else if port_name is not None: do a trade according to the port type and resource_1 and resource_2
    returns True if trade was successful, otherwise prints out what went wrong and returns false.
    """
    def trade(self, player_id, resource_1, resource_2, other_player_id=-1, port_name=None):
        return True

#b = game.player_list[0].backpack
#print(b), can't print out actual information for some reason

"""
Returns the sum of two dice rolls
"""
def roll_dice():
    rolls = np.random.choice([1, 2, 3, 4, 5, 6], 2)
    return rolls[0] + rolls[1]

"""
Decides which player goes first
returns the player_id that wins
"""
def _starter(player_ids):
    highest_roll = 0
    player_rolls = {}
    while len(player_ids) > 1:
        for player in player_ids:
            r = roll_dice()
            player_rolls[player] = r
            highest_roll = r if r > highest_roll else highest roll
        player_ids = [k for k, v in player_rolls.items() if v == highest_roll]
        highest_roll = 0
        player_rolls.clear()
    return player_ids[0]

"""
Takes care of user experience; given a player and action
perform the given action, returns True if done otherwise False or an action
"""
def _ux(player_id, action):
    actions = ["build road", "build settlement", "build city", "buy dev card", "use dev card", "trade", "done"]
    trades = ["player", "port", "4:1"]
    ports = ["wheat", "sheep", "ore", "clay", "wood", "3:1"]

    if action == "ask for action":
        response = input("Player %s, what would you like to do? " % player_id)
        while response.lower() not in actions:
            response = input("That's not a valid action, please choose one from the following: %s" % actions)
        return response

    elif action == "done":
        return True
    elif action.split(" ")[0] == "build":
        obj = action.split(" ")[1]
        build_location = input("Player %s, where would you like to build your %s ? " % (player_id, obj))
        if obj == "settlement":            
            while not build_settlement(player_id, build_location):
                build_location = input("Sorry, you cannot build there, please choose another location: ")
        elif obj == "city":
            while not build_city(player_id, build_location):
                build_location = input("Sorry, you cannot build there, please choose another location: ")
        elif obj == "road":
            while not build_road(player_id, build_location):
                build_location = input("Sorry, you cannot build there, please choose another location: ")

    elif action == "buy dev card":
        buy_dev_card(player_id)

    elif action == "use dev card":
        use_dev_card(player_id)

    elif action == "trade": #TODO
        response = input("What type of trade would you like to do? ")
        while response.lower() not in trades:
            response = input("That's not a valid trade, please choose from the following: %s" % trades)
        if response == "player":
            response = input("")
        elif response == "port":
            response = input("Which port would you like to use? ")
            while response.lower() not in ports:
                response = input("That's not a valid port, please choose from the following: %s" % ports)            
        elif response == "4:1":
            response = input("")
    return False



