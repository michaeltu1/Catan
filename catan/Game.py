import numpy as np
from catan.Player import Player
from catan.Inventory import Inventory
from catan.Board import Board


class Game:
    def __init__(self):
        self.unbuildable = set()

        resource_cards = {"Wheat": 19, "Sheep": 19, "Ore": 19, "Clay": 19, "Wood": 19}
        dev_cards = {"Knight": 14, "Victory Point": 5, "Road Building": 2, "Year of Plenty": 2, "Monopoly": 2}

        self.game_resources = Inventory(resource_cards, dev_cards)
        self.board = Board()
        self.tiles = self.board.land_tiles
        self.edges = self.board.edges
        self.intersections = self.board.intersections
        self.player_list = {}
        self.game_over = False

    def play(self, num_players):
        # Create players, player_id starts at 1
        for number in range(num_players):
            player = Player(number)
            self.player_list[number] = player

        # Decide who goes first
        player_first = self._starter(self.player_list.keys())
        
        # First round of choosing settlements and roads
        for player_id in range(player_first, player_first + num_players):
            player_id %= num_players
            self.__ux(player_id, "build settlement")
            self.__ux(player_id, "build road")

        # Second round of choosing settlements and roads
        for player_id in reversed(range(player_first, player_first + num_players)):
            player_id %= num_players
            self.__ux(player_id, "build settlement")

            # Get the rolls num associated with the tiles that the settlement are touching
            # and give those resources to the player
            for roll_num in self.player_list[player_id].backpack.rolls.keys():
                self.distribute_resources(player_id, roll_num)
            self.__ux(player_id, "build road")
        
        while not self.game_over:
            # TODO: Robber when dice roll is 7
            for player_id in range(player_first, player_first + num_players):
                r = self.roll_dice()
                self.distribute_resources(player_id, r)

                done = False
                while not done:
                    action = self.__ux(player_id, "ask for action")
                    done = self.__ux(player_id, action)

                if self.player_list[player_id].backpack.victory_points == 10:
                    self.game_over = True
                    print("Player %s has won the game" % player_id)

    """
    Returns the sum of two dice rolls
    """
    def roll_dice(self):
        return np.random.choice(np.arange(13), p=self.board.distribution)

    """
    Given a player and roll_num, distribute resources according to what tiles the player owns
    """
    def distribute_resources(self, player_id, roll_num):
        player = self.player_list[player_id]
        rolls = player.backpack.rolls
        if roll_num in rolls:
            tiles = rolls[roll_num]  # set of tile ids
            for tile in tiles:
                resource = self.tiles[tile].resource_type 
                quantity = player.backpack.tiles[tile]
                remaining = self.game_resources.resource_cards[resource]
                if remaining == 0:
                    print("No more %s left" % resource)
                elif remaining < quantity:
                    print("There's only %s %s left" % (quantity, resource))
                self.game_resources.resource_cards[resource] -= min(quantity, remaining)
                if resource not in player.backpack.resource_cards:
                    player.backpack.resource_cards[resource] = 0
                player.backpack.resource_cards[resource] += min(quantity, remaining)

    """
    Take in a player_id and attempt to build a road at an edge tuple (x, y)
    Need to update player's backpack's num_roads, roads
    returns true if successful, otherwise false.
    
    Todo: check longest road
    """
    def build_road(self, player_id, edge):
        # Edge needs to exist and not have a road, and player needs to have the resource to build the road
        player_bp = self.player_list[player_id].backpack
        if edge in self.edges and not self.edges[edge].has_road:
            if "Wood" in player_bp.resource_cards and player_bp.resource_cards["Wood"] > 0 and \
                    "Clay" in player_bp.resource_cards and player_bp.resource_cards["Clay"] > 0:
                if player_bp.num_roads > 0:
                    self.edges[edge].has_road = True
                    player_bp.resource_cards["Wood"] -= 1
                    player_bp.resource_cards["Clay"] -= 1
                    self.game_resources.resource_cards["Wood"] += 1
                    self.game_resources.resource_cards["Clay"] += 1
                    player_bp.num_roads -= 1
                    player_bp.roads.add(edge)
                    return True
                else:
                    print("You don't have any more spare roads")
            else:
                print("You don't have the required resource of 1 Wood and 1 Clay")
        else:
            print("That's not a valid spot for a road or the spot already has a road on it")
        return False

    """
    Take in a player_id and attempt to build a settlement at an intersection tuple (x, y, z)
    Need to update player's backpack's num_settlements, victory_points, rolls, tiles, and ports if applicable
    returns true if successful, otherwise false.

    # Todo: check longest road
    """

    def build_settlement(self, player_id, intersection):

        player_bp = self.player_list[player_id].backpack
        if intersection in self.intersections and intersection not in self.unbuildable:
            int_obj = self.intersections[intersection]
            if "Wood" in player_bp.resource_cards and player_bp.resource_cards["Wood"] > 0 and \
                    "Clay" in player_bp.resource_cards and player_bp.resource_cards["Clay"] > 0 and \
                    "Wheat" in player_bp.resource_cards and player_bp.resource_cards["Wheat"] > 0 and \
                    "Sheep" in player_bp.resource_cards and player_bp.resource_cards["Sheep"] > 0:
                if player_bp.num_settlements > 0:
                    # Add intersections that cannot be built anymore
                    self.unbuildable.add(intersection)
                    if (int_obj.intersect_ID[0] + int_obj.intersect_ID[1]) % 2 != 0:
                        self.unbuildable.add((int_obj.intersect_ID[0], int_obj.intersect_ID[1] - 7, int_obj.intersect_ID[2]))
                        self.unbuildable.add((int_obj.intersect_ID[0] - 2, int_obj.intersect_ID[0], int_obj.intersect_ID[1]))
                        self.unbuildable.add((int_obj.intersect_ID[1], int_obj.intersect_ID[2], int_obj.intersect_ID[2] + 9))
                    else:
                        self.unbuildable.add((int_obj.intersect_ID[1], int_obj.intersect_ID[2], int_obj.intersect_ID[2] + 2))
                        self.unbuildable.add((int_obj.intersect_ID[0] - 9, int_obj.intersect_ID[0], int_obj.intersect_ID[1]))
                        self.unbuildable.add((int_obj.intersect_ID[0], int_obj.intersect_ID[1] + 7, int_obj.intersect_ID[2]))
                    int_obj.has_settlement = True

                    # Take player's resources and add them to game resources
                    player_bp.resource_cards["Wood"] -= 1
                    player_bp.resource_cards["Clay"] -= 1
                    player_bp.resource_cards["Wheat"] -= 1
                    player_bp.resource_cards["Sheep"] -= 1
                    self.game_resources.resource_cards["Wood"] += 1
                    self.game_resources.resource_cards["Clay"] += 1
                    self.game_resources.resource_cards["Wheat"] += 1
                    self.game_resources.resource_cards["Sheep"] += 1

                    for tile in intersection:
                        # Check if tile is not a desert
                        if self.tiles[tile].resource_type != "Desert":
                            t_obj = self.tiles[tile]
                            # Add roll_num to player rolls dictionary
                            if t_obj.roll_num not in player_bp.rolls:
                                player_bp.rolls[t_obj.roll_num] = set()
                            player_bp.rolls[t_obj.roll_num].add(t_obj.tile_id)
                            # Add tile to player tile dictionary
                            if t_obj.tile_id not in player_bp.tiles:
                                player_bp.tiles[t_obj.tile_id] = 0
                            player_bp.tiles[t_obj.tile_id] += 1
                    # Add port if it exists
                    if int_obj.port is not None:
                        player_bp.ports.add(int_obj.port)

                    player_bp.num_settlements -= 1
                    player_bp.settlements.add(intersection)
                    player_bp.victory_points += 1
                    return True
                else:
                    print("You don't have any spare settlements")
            else:
                print("You don't have the required resource of 1 Wood, Clay, Wheat and Sheep")
        else:
            print("That's not a valid spot for a new settlement")
        return False

    """
    Take in a player_id and attempt to build a city at an intersection tuple (x, y, z)
    returns true if successful, otherwise false.
    """

    def build_city(self, player_id, intersection):
        player_bp = self.player_list[player_id].backpack
        if intersection in player_bp.settlements:
            if self.intersections[intersection].has_settlement:
                if "Ore" in player_bp.resource_cards and player_bp.resource_cards["Ore"] > 2 and \
                        "Wheat" in player_bp.resource_cards and player_bp.resource_cards["Wheat"] > 1:
                    # Convert settlement to city
                    self.intersections[intersection].has_settlement = False
                    self.intersections[intersection].has_city = True
                    player_bp.resource_cards["Ore"] -= 3
                    player_bp.resource_cards["Wheat"] -= 2
                    self.game_resources.resource_cards["Ore"] += 3
                    self.game_resources.resource_cards["Wheat"] += 2

                    # Update player Tiles
                    for tile in intersection:
                        if self.tiles[tile].resource_type != "Desert":
                            t_obj = self.tiles[tile]
                            player_bp.tiles[t_obj.tile_id] += 1
                    player_bp.num_settlements += 1
                    player_bp.num_cities -= 1
                    player_bp.victory_points += 1
                    return True
                else:
                    print("You don't have the required resource of 3 Ores and 2 Wheat")
            else:
                print("You already have a city here")
        else:
            print("You don't own a settlement here")
            intersection.has_settlement = False
            intersection.has_city = True
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

    """
    TODO: Cancel operation
    Takes care of user experience; given a player and action
    perform the given action, returns True if done otherwise False or an action
    """
    def __ux(self, player_id, action):
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
                while not self.build_settlement(player_id, build_location):
                    build_location = input("Sorry, you cannot build there, please choose another location: ")
            elif obj == "city":
                while not self.build_city(player_id, build_location):
                    build_location = input("Sorry, you cannot build there, please choose another location: ")
            elif obj == "road":
                while not self.build_road(player_id, build_location):
                    build_location = input("Sorry, you cannot build there, please choose another location: ")

        elif action == "buy dev card":
            self.buy_dev_card(player_id)

        elif action == "use dev card":
            self.use_dev_card(player_id)

        elif action == "trade":  # TODO
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

# b = game.player_list[0].backpack
# print(b), can't print out actual information for some reason

    """
    Decides which player goes first
    returns the player_id that wins
    """
    def _starter(self, player_ids):
        highest_roll = 0
        player_rolls = {}
        while len(player_ids) > 1:
            for player in player_ids:
                r = self.roll_dice()
                player_rolls[player] = r
                highest_roll = r if r > highest_roll else highest_roll
            player_ids = [k for k, v in player_rolls.items() if v == highest_roll]
            highest_roll = 0
            player_rolls.clear()
        return player_ids[0]

if __name__ == "__main__":
    g = Game()
    p = Player(0)
    g.player_list[0] = p
    p.backpack.resource_cards["Wood"] = 1
    p.backpack.resource_cards["Clay"] = 2
    p.backpack.resource_cards["Wheat"] = 5
    p.backpack.resource_cards["Sheep"] = 4
    p.backpack.resource_cards["Ore"] = 3
    g.build_settlement(0, (-11, -2, 0))
    g.build_city(0, (-11, -2, 0))
    print(g.game_resources)
    print(p.backpack)