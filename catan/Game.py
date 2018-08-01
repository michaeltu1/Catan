import numpy as np
import json

from ast import literal_eval
from collections import defaultdict
from json import JSONEncoder


from catan.Player import Player
from catan.Inventory import Inventory
from catan.Board import Board
from catan.DevCard import DevCard
from catan.Tile import Tile
from catan.Edge import Edge
from catan.Intersection import Intersection


class Game:
    # TODO Make regex for resources or convert them to lowercase in board
    def __init__(self):
        self.unbuildable = set()

        resource_cards = {"Wood": 19, "Clay": 19, "Wheat": 19, "Sheep": 19, "Ore": 19}
        self.game_dev_cards = {"Knight": 14, "Victory Point": 5, "Road Building": 2, "Year of Plenty": 2, "Monopoly": 2}

        dev_cards = DevCard.craft("Knight", 14) + DevCard.craft("Victory Point", 5) + \
                    DevCard.craft("Road Building", 2) + DevCard.craft("Year of Plenty", 2) + \
                    DevCard.craft("Monopoly", 2)

        self.game_resources = Inventory(resource_cards, dev_cards)
        self.board = Board()
        self.tiles = self.board.land_tiles
        self.edges = self.board.edges
        self.intersections = self.board.intersections
        self.player_list = {}
        self.robber = self.board.robber_tile
        self.has_longest_road = None
        self.has_largest_army = None
        self.game_over = False

    def play(self, num_players):
        # Create players, player_id starts at 1
        for number in range(num_players):
            player = Player(number)
            self.player_list[number] = player
            player.backpack.resource_cards["Wood"] = 0
            player.backpack.resource_cards["Clay"] = 0
            player.backpack.resource_cards["Wheat"] = 0
            player.backpack.resource_cards["Sheep"] = 0
            player.backpack.resource_cards["Ore"] = 0

        # Decide who goes first
        player_first = self.__starter(self.player_list.keys())

        print(self.board)
        print(self.tiles)
        print(self.edges)
        print(self.board.intersections)
        # First round of choosing settlements and roads
        for player_id in range(player_first, player_first + num_players):
            player_id %= num_players
            self.__ux(player_id, "build starting_settlement")
            self.__ux(player_id, "build roads")

        # Second round of choosing settlements and roads
        for player_id in reversed(range(player_first, player_first + num_players)):
            player_id %= num_players
            second_settlement = self.__ux(player_id, "build starting_settlement", True)

            # Get the resources associated with the tiles that the settlement are touching
            # and give those resources to the player
            resources = [self.tiles[tile_id].resource_type for tile_id in second_settlement]
            print(resources)

            for resource in resources:
                if resource != "Desert":
                    self.player_list[player_id].backpack.resource_cards[resource] += 1
                    self.game_resources.resource_cards[resource] -= 1

            # Check to make sure this road is connected to the second settlement
            self.__ux(player_id, "build second_road", second_settlement)
        
        while not self.game_over:
            for player_id in range(player_first, player_first + num_players):
                player_id %= num_players
                r = self.roll_dice()
                print("Player {0} has rolled a {1} \n".format(player_id, r))
                if r == 7:
                    self.return_resources()
                    self.move_robber(player_id)
                else:
                    for pid in range(player_first, player_first + num_players):
                        pid %= num_players
                        self.distribute_resources(pid, r)

                done = False
                while not done:
                    action = self.__ux(player_id, "ask for action")
                    done = self.__ux(player_id, action)
                self.player_list[player_id].dev_cards_used = False
                self.player_list[player_id].turn_number += 1
                # optimize check
                # After a player has built at least 5 roads, check at the end of each turn
                if self.player_list[player_id].backpack.num_roads <= 10:
                    self.check_longest_road(player_id)

                if self.player_list[player_id].backpack.victory_points >= 10:
                    self.game_over = True
                    print("Player %s has won the game \n" % player_id)

    """
    Returns the sum of two dice rolls
    """
    def roll_dice(self):
        return np.random.choice(np.arange(13), p=self.board.distribution)

    """
    Find the tile the robber is located on
    """
    # TODO: Store the location of the robber at self.robber and remove this function
    def find_robber(self):
        for tile in self.tiles.values():
            if tile.has_robber:
                return tile.tile_id

    def move_robber(self, player_id):
        self.__ux(player_id, "move robber")

    """
    Steal a random card from another player's hand
    """
    def steal(self, player_id, other_player):
        other_resources = self.player_list[other_player].backpack.resource_cards
        total = np.sum(list(other_resources.values()))
        # Choose randomly from other player's cards
        resource = list(other_resources)[np.random.choice(np.arange(5), p=list(other_resources.values()) / total)]
        other_resources[resource] -= 1
        self.player_list[player_id].backpack.resource_cards[resource] += 1
        print("Player {} got {} from player {}".format(player_id, resource, other_player))

    """
    Given a player and roll_num, distribute resources according to what tiles the player owns
    """

    # TODO: If not all players can be given the exact number of resources of some type
    #       that they should receive, then no player collects resources of that type
    #       i.e. 'quantity' has to be sum(p0's quantity, p1's quantity, p2's quantity, and p3's quantity)
    def distribute_resources(self, player_id, roll_num):
        player = self.player_list[player_id]
        rolls = player.backpack.rolls
        if roll_num in rolls:
            tiles = rolls[roll_num]  # set of tile ids
            for tile in tiles:
                if not self.tiles[tile].has_robber:
                    resource = self.tiles[tile].resource_type
                    quantity = player.backpack.tiles[tile]
                    remaining = self.game_resources.resource_cards[resource]
                    if remaining == 0:
                        print("No more {0} left \n".format(resource))
                    elif remaining < quantity:
                        print("There's only {0} {1} left \n".format(quantity, resource))
                    self.game_resources.resource_cards[resource] -= min(quantity, remaining)
                    player.backpack.resource_cards[resource] += min(quantity, remaining)
                    player.backpack.num_cards += min(quantity, remaining)
                    print("Player {} got {} {}".format(player_id, quantity, resource))

    """
    Every player that has more than 7 cards, must return half (rounded down) of their cards to the bank
    """
    def return_resources(self):
        for player_id in self.player_list:
            player_bp = self.player_list[player_id].backpack
            if player_bp.num_cards > 7:
                self.__ux(player_id, "return resources")


    # TODO make an arbitrary add/remove resource function
    """
    Take in a player_id and attempt to build a road at an edge tuple (x, y)
    Need to update player's backpack's num_roads, roads
    returns true if successful, otherwise false.
    
    Todo: check longest road, check if connected to rest of player's road/settlement
    """
    def build_road(self, player_id, edge, dev_card=False, second_settlement=None):
        # Edge needs to exist and not have a road, and player needs to have the resource to build the road
        player_bp = self.player_list[player_id].backpack

        # TODO: Fix style
        if edge in self.edges and not self.edges[edge].has_road and self.__connected(player_id, edge, second_settlement):
            if dev_card or (player_bp.resource_cards["Wood"] > 0 and player_bp.resource_cards["Clay"] > 0):
                if player_bp.num_roads > 0:
                    self.edges[edge].has_road = True
                    if not dev_card:
                        player_bp.resource_cards["Wood"] -= 1
                        player_bp.resource_cards["Clay"] -= 1
                        self.game_resources.resource_cards["Wood"] += 1
                        self.game_resources.resource_cards["Clay"] += 1
                        player_bp.num_cards -= 2
                    player_bp.num_roads -= 1
                    player_bp.roads.add(edge)
                    return True
                else:
                    print("You don't have any more spare roads \n")
            else:
                print("You don't have the required resource of 1 Wood and 1 Clay \n")
        else:
            print("That's not a valid spot for a road or the spot already has a road on it \n")
        return False

    """
    Check if a given edge is connected to the rest of the player's roads/settlement
    """
    def __connected(self, player_id, edge, second_settlement=None):
        player_bp = self.player_list[player_id].backpack
        # Special case where road has to be next to a specific settlement
        # print(second_settlement)
        if second_settlement is not None:
            if self.edges[edge].edge_ID[0] in second_settlement and self.edges[edge].edge_ID[1] in second_settlement:
                return True
            else:
                return False
        # Check if connected to a settlement
        for intersect in player_bp.settlements:
            if self.edges[edge].edge_ID[0] in intersect and self.edges[edge].edge_ID[1] in intersect:
                return True
        # Check if connected to a road
        for road in player_bp.roads:
            if self.edges[edge].adjacent_edge(road):
                return True
        return False

    def check_longest_road(self, player_id):
        roads = self.player_list[player_id].backpack.roads
        road_length = 0

        graph = defaultdict(set)

        for edge in roads:
            x, y = edge.get_vertices()
            graph[x].add(y)
            graph[y].add(x)
        # TODO: cache the graph

        vertex_degrees = {v: len([e for e in v.adjacent_edges() if e in roads]) for v in graph.keys()}

        dfs_starting_points = [k for k in vertex_degrees.keys() if vertex_degrees[k] == 1] or \
                              [k for k in vertex_degrees.keys() if vertex_degrees[k] == 2]

        for vertex in dfs_starting_points:
            road_length = max(road_length, self.__dfs(graph, vertex))

        # Update player's road length
        self.player_list[player_id].road_length = road_length

        # TODO: Update player's road length (check if settlement blocked road)

        # TODO:  check length >= 5 somewhere before calling this function
        if self.has_longest_road is None:
            self.has_longest_road = player_id
            self.player_list[player_id].backpack.victory_points += 2
        else:
            current_longest = self.player_list[self.has_longest_road]
            # Check if they are not the same person?
            if road_length > current_longest.road_length:
                current_longest.backpack.victory_points -= 2
                self.player_list[player_id].backpack.victory_points += 2
                self.has_longest_road = player_id

    def __dfs(self, graph, starting_vertex, visited=None, depth=0):
        visited = visited or [starting_vertex]
        for vertex in graph[starting_vertex]:
            if vertex in visited:
                return depth
            else:
                d = self.__dfs(graph, starting_vertex, depth + 1, visited + [vertex])
                depth = max(depth, d)
        return depth

    """
    Take in a player_id and attempt to build a settlement at an intersection tuple (x, y, z)
    Need to update player's backpack's num_settlements, victory_points, rolls, tiles, and ports if applicable
    returns true if successful, otherwise false.

    # Todo: check longest road
    """

    def build_settlement(self, player_id, intersection, game_start=False):
        player_bp = self.player_list[player_id].backpack
        if intersection in self.intersections and intersection not in self.unbuildable:
            int_obj = self.intersections[intersection]
            if game_start or (player_bp.resource_cards["Wood"] > 0 and player_bp.resource_cards["Clay"] > 0 and
                              player_bp.resource_cards["Wheat"] > 0 and player_bp.resource_cards["Sheep"] > 0):
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
                    if not game_start:
                        player_bp.resource_cards["Wood"] -= 1
                        player_bp.resource_cards["Clay"] -= 1
                        player_bp.resource_cards["Wheat"] -= 1
                        player_bp.resource_cards["Sheep"] -= 1
                        self.game_resources.resource_cards["Wood"] += 1
                        self.game_resources.resource_cards["Clay"] += 1
                        self.game_resources.resource_cards["Wheat"] += 1
                        self.game_resources.resource_cards["Sheep"] += 1
                        player_bp.num_cards -= 4

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
                    print("You don't have any spare settlements \n")
            else:
                print("You don't have the required resource of 1 Wood, Clay, Wheat and Sheep \n")
        else:
            print("That's not a valid spot for a new settlement \n")
        return False

    """
    Take in a player_id and attempt to build a city at an intersection tuple (x, y, z)
    returns true if successful, otherwise false.
    """

    def build_city(self, player_id, intersection):
        player_bp = self.player_list[player_id].backpack
        if intersection in player_bp.settlements:
            if self.intersections[intersection].has_settlement:
                if player_bp.resource_cards["Ore"] > 2 and player_bp.resource_cards["Wheat"] > 1:
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
                    player_bp.num_cards -= 5
                    player_bp.num_settlements += 1
                    player_bp.num_cities -= 1
                    player_bp.victory_points += 1

                    intersection.has_settlement = False
                    intersection.has_city = True
                    return True
                else:
                    print("You don't have the required resource of 3 Ores and 2 Wheat \n")
            else:
                print("You already have a city here \n")
        else:
            print("You don't own a settlement here \n")
        return False

    """
    Take in a player_id and attempt to buy a dev card
    returns the index of the player's dev_card location in their backpack
    so the game can activate it at the end of the turn if successful, otherwise returns false
    """
    def buy_dev_card(self, player_id):
        player_bp = self.player_list[player_id].backpack
        if player_bp.resource_cards["Ore"] > 0 and player_bp.resource_cards["Sheep"] > 0 \
                and player_bp.resource_cards["Wheat"] > 0:
            # Pick a random dev card from the game resource
            dev_cards = self.game_resources.dev_cards

            if len(dev_cards) > 0:
                player_bp.resource_cards["Ore"] -= 1
                player_bp.resource_cards["Sheep"] -= 1
                player_bp.resource_cards["Wheat"] -= 1
                self.game_resources.resource_cards["Ore"] += 1
                self.game_resources.resource_cards["Sheep"] += 1
                self.game_resources.resource_cards["Wheat"] += 1

                index = np.random.randint(0, len(dev_cards))
                card_obj = dev_cards.pop(index)
                card_obj.turn_bought = self.player_list[player_id].turn_number

                player_bp.num_cards -= 3
                player_bp.dev_cards.append(card_obj)
                self.game_dev_cards[card_obj.card_type] -= 1
                return True
            else:
                print("There are no more dev cards to buy \n")
        else:
            print("You don't have the required resource of 1 Ore, Sheep, and Wheat \n")
        return False

    """
    Take in a player_id and use a dev card
    make sure that the card wasn't bought in the same turn
    returns true if used successfully, otherwise returns false
    """

    def use_dev_card(self, player_id, card):
        player = self.player_list[player_id]
        index = self.__find_usable_dev_card(player_id, card)
        success = False
        if index is not None:
            if card == "victory point":
                player.backpack.victory_points += 1
                player.backpack.dev_cards(index)
            elif not player.dev_cards_used:
                if card == "knight":
                    self.move_robber(player_id)
                    self.player_list[player_id].knights_played += 1
                    if self.player_list[player_id].knights_played >= 3:
                        self.check_largest_army(player_id)
                    player.dev_cards_used = True
                    player.backpack.dev_cards[index].used = True
                    return True
                elif card == "road building":
                    # Don't have a way of canceling after only one road is built
                    self.__ux(player_id, "build roads")
                    self.__ux(player_id, "build roads")
                    success = True
                elif card == "year of plenty":
                    success = self.__ux(player_id, "year of plenty")
                elif card == "monopoly":
                    success = self.__ux(player_id, "monopoly")

                if success:
                    player.dev_cards_used = True
                    player.backpack.dev_cards.pop(index)
                return True
            else:
                print("You already used a dev card this turn \n")
        else:
            print("You don't own that card or you can't use it this turn \n")
            self.__ux(player_id, "use dev card")

        return False

    """
    Returns the index in the player's dev_card list that corresponds to a usable dev card,
    Returns None if cannot find one
    """
    def __find_usable_dev_card(self, player_id, card):
        player_bp = self.player_list[player_id].backpack
        for index in range(len(player_bp.dev_cards)):
            if (card == "victory point" or player_bp.dev_cards[index].turn_bought !=
                    self.player_list[player_id].turn_number) and player_bp.dev_cards[index].card_type.lower() == card:
                return index

    """
    Check who has the largest army currently and update victory points and titles accordingly
    """
    def check_largest_army(self, player_id):
        if self.has_largest_army is None:
            self.player_list[player_id].backpack.victory_points += 2
            self.has_largest_army = player_id
        else:
            current = self.player_list[self.has_largest_army].knights_played
            if self.player_list[player_id].knights_played > current:
                self.player_list[self.has_largest_army].backpack.victory_points -= 2
                self.player_list[player_id].backpack.victory_points += 2
                self.has_largest_army = player_id

    """
    Takes care of user experience; given a player and action
    perform the given action, returns True if done otherwise False or an action
    """
    def __ux(self, player_id, action, second_settlement=None):
        actions = ["build road", "build settlement", "build city", "buy dev card",
                   "use dev card", "check resources", "trade", "done"]
        trades = ["player", "port", "4:1"]
        resources = ["wheat", "sheep", "ore", "clay", "wood"]
        ports = resources + ["3:1"]
        dev_cards = ["victory point", "knight", "road building", "year of plenty", "monopoly"]
        players = list(self.player_list.keys())

        if action == "ask for action":
            response = input("Player %s, what would you like to do? \n" % player_id)
            while response.lower() not in actions:
                response = input("That's not a valid action, please choose one from the following: %s \n" % actions)
            return response

        elif action == "done":
            return True

        elif action.split(" ")[0] == "build":
            obj = action.split(" ")[1]
            build_location = input("Player %s, where would you like to build your %s? \n" % (player_id, obj))
            if build_location == "cancel":
                return False
            if obj == "settlement":
                while not self.build_settlement(player_id, literal_eval(build_location)):
                    build_location = input("Sorry, you cannot build there, please choose another location: \n")
                    if build_location == "cancel":
                        break
            elif obj == "starting_settlement":
                while not self.build_settlement(player_id, literal_eval(build_location), True):
                    build_location = input("Sorry, you cannot build there, please choose another location: \n")
                    if build_location == "cancel":
                        break
                if second_settlement is not None and build_location != "cancel":
                    return literal_eval(build_location)
            elif obj == "city":
                while not self.build_city(player_id, literal_eval(build_location)):
                    build_location = input("Sorry, you cannot build there, please choose another location: \n")
                    if build_location == "cancel":
                        break
            elif obj == "road":
                while not self.build_road(player_id, literal_eval(build_location)):
                    build_location = input("Sorry, you cannot build there, please choose another location: \n")
                    if build_location == "cancel":
                        break
            elif obj == "roads":
                while not self.build_road(player_id, literal_eval(build_location), True):
                    build_location = input("Sorry, you cannot build there, please choose another location: \n")
                    if build_location == "cancel":
                        break
            elif obj == "second_road":
                while not self.build_road(player_id, literal_eval(build_location), True, second_settlement):
                    build_location = input("Sorry, you cannot build there, please choose another location: \n")
                    if build_location == "cancel":
                        break

        elif action == "buy dev card":
            self.buy_dev_card(player_id)

        elif action == "use dev card":
            card = input("Which dev card would you like to use? You have: %s \n"
                         % self.player_list[player_id].backpack.dev_cards)
            if card == "cancel":
                return False
            while card.lower() not in dev_cards:
                card = input("Please select a valid dev card: %s \n" % dev_cards)
                if card == "cancel":
                    return False
            self.use_dev_card(player_id, card)

        elif action == "year of plenty":
            resource_lst = []
            while len(resource_lst) != 2:
                resource = input("Choose a resource: \n")
                resource = resource.split(" ")
                if resource == "cancel":
                    return False
                while len(resource) != 1:
                    resource = input("One at a time please: \n")
                    resource = resource.split(" ")
                    if resource == "cancel":
                        return False
                resource = resource[0]
                while resource not in resources:
                    resource = input("That's not a valid resource, try again: \n")
                    if resource == "cancel":
                        return False
                resource = resource[0].upper() + resource[1:]
                if self.game_resources.resource_cards[resource] > 0:
                    resource_lst += [resource]
                else:
                    print("There's no more %s, choose another resource: \n" % resource)
            r_1 = resource_lst[0]
            r_2 = resource_lst[1]
            r_1 = r_1[0].upper() + r_1[1:]
            r_2 = r_2[0].upper() + r_2[1:]

            player_resources = self.player_list[player_id].backpack.resource_cards
            player_resources[r_1] += 1
            player_resources[r_2] += 1
            self.player_list[player_id].backpack.num_cards += 2
            self.game_resources.resource_cards[r_1] -= 1
            return True

        elif action == "monopoly":
            resource = input("What resource would you like? \n")
            while resource not in resources:
                resource = input("That's not a valid resource, try again: \n")
                if resource == "cancel":
                    return False
            resource = resource[0].upper() + resource[1:]

            for player in self.player_list:
                player_resources = self.player_list[player].backpack.resource_cards
                if player != player_id:
                    amount = player_resources[resource]
                    self.player_list[player_id].backpack.num_cards += amount
                    self.player_list[player_id].backpack.resource_cards[resource] += amount
                    player_resources[resource] = 0
            return True

        elif action == "move robber":
            move_location = literal_eval(input("Where would you like to move the robber? \n"))
            while move_location not in self.tiles:
                move_location = literal_eval(input("That's not a valid tile id \n"))
            self.robber = move_location
            steal_lst = []
            for player in self.player_list:
                if player != player_id:
                    for settlement in self.player_list[player].backpack.settlements:
                        if move_location in settlement:
                            steal_lst += [player]

            if len(steal_lst) == 0:
                print("No player to steal from \n")
                return False
            player = literal_eval(input("You can steal from player(s): %s \n" % steal_lst))
            while player not in steal_lst:
                player = literal_eval(input("That's not one of the options, try again \n"))
            self.steal(player_id, player)

        elif action == "return resources":
            player_bp = self.player_list[player_id].backpack
            leftover_amount = player_bp.num_cards - player_bp.num_cards // 2
            while player_bp.num_cards > leftover_amount:
                resource = input("Player %s, you need to get rid of %s resources, what resource "
                                 "are you getting rid of? \n" % (player_id, player_bp.num_cards - leftover_amount))
                while resource.lower() not in resources:
                    resource = input("That's not a valid resource, try again: \n")
                resource = resource[0].upper() + resource[1:]
                if player_bp.resource_cards[resource] > 0:
                    player_bp.num_cards -= 1
                    player_bp.resource_cards[resource] -= 1
                    self.game_resources.resource_cards[resource] += 1
                else:
                    print("You don't have anymore of those! \n")

        elif action == "check resources":
            print(self.player_list[player_id].backpack)

        elif action == "trade":  # TODO check for valid trades
            response = input("What type of trade would you like to do? \n")
            if response == "cancel":
                return False
            while response.lower() not in trades:
                response = input("That's not a valid trade, please choose from the following: %s \n" % trades)
                if response == "cancel":
                    return False
            if response == "player":
                response = input("Which player would you like to trade with? {} \n".format(players))
                while literal_eval(response) not in players:
                    response = input("That's not a valid player, try again: \n")
                    if response == "cancel":
                        return False
                other_player = literal_eval(response)
                giving = {}
                receiving = {}
                types = literal_eval(input("How many types of resources are you giving up? \n"))
                giving = self.trade_agreement(types)
                types = literal_eval(input("How many types of resources are you receiving? \n"))
                receiving = self.trade_agreement(types)
                response = input("Player {}, player {} wants to trade {} for {}, do you agree? \n"
                                 .format(other_player, player_id, giving, receiving))
                if response.lower().startswith("y"):
                    for resource in giving:
                        amount = giving[resource]
                        # Not checking if both players have the resources required for the trade
                        self.player_list[player_id].backpack.resource_cards[resource] -= amount
                        self.player_list[other_player].backpack.resource_cards[resource] += amount
                    for resource in receiving:
                        amount = receiving[resource]
                        resource = resource[0].upper() + resource[1:]
                        self.player_list[player_id].backpack.resource_cards[resource] += amount
                        self.player_list[other_player].backpack.resource_cards[resource] -= amount

            elif response == "port":
                response = input("Which port would you like to use? \n")
                while response.lower() not in ports:
                    response = input("That's not a valid port, please choose from the following: %s \n" % ports)
                if response == "3:1":
                    self.single_type_trade(player_id, 3)
                else:
                    response = response[0].upper() + response[1:]
                    if response not in self.player_list[player_id].backpack.ports:
                        print("You don't own this port")
                        return False
                    else:
                        self.single_type_trade(player_id, 2, response)
            elif response == "4:1":
                self.single_type_trade(player_id, 4)
        return False

    def single_type_trade(self, player_id, ratio, resource_type=None):
        print("What are you giving up? \n")
        giving = self.trade_agreement()

        resource = list(giving.keys())[0]
        if resource_type is not None:
            if resource_type != resource:
                print("You can't use this {} port to trade {} resource! \n".format(resource_type, resource))
                return False
        amount = giving[resource] // ratio
        resources = self.game_resources.resource_cards.keys()
        response = input("What do you want for it? \n")
        response = response[0].upper() + response[1:]
        while response not in resources:
            response = input("That's not a valid resource \n")
        response = response[0].upper() + response[1:]
        accept = input("Trade {} {} for {} {} ? \n".format(amount * ratio, resource, response, amount))
        if accept.lower().startswith("y"):
            self.player_list[player_id].backpack.resource_cards[resource] -= amount * ratio
            self.player_list[player_id].backpack.resource_cards[response] += amount

    def trade_agreement(self, types=1):
        trade_dict = {}
        resources = self.game_resources.resource_cards.keys()
        for resource in range(types):
            resource_type = input("Resource type {}? \n".format(resources))
            resource_type = resource_type[0].upper() + resource_type[1:]
            while resource_type not in resources:
                resource_type = input("That's not a valid resource \n")
            quantity = literal_eval(input("How many? \n"))
            trade_dict[resource_type] = quantity
        return trade_dict

    """
    Decides which player goes first
    returns the player_id that wins
    """
    def __starter(self, player_ids):
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


class GameEncoder(JSONEncoder):
    def default(self, o):
        if isinstance(o, Game):
            return {'unbuildable':      str(o.unbuildable),
                    'game_dev_cards':   str(o.game_dev_cards),
                    'game_resources':   str(o.game_resources.__repr__()),
                    'board':            str(o.board.__repr__()), # needs repr
                    'tiles':            str(o.tiles),
                    'edges':            str(o.edges),
                    'intersections':    str(o.intersections),
                    'player_list':      str(o.player_list),
                    'robber':           str(o.robber),
                    'has_longest_road': str(o.has_longest_road),
                    'has_largest_army': str(o.has_largest_army),
                    'game_over':        str(o.game_over)}
        raise NotImplementedError


def eval_intersection_objects(bored, attr, s, ret_val=False):
    val = []
    s = s.strip("[Intersection]")
    s = s.replace(", I", "I")
    s = s.split("Intersection")
    for params in s:
        params = params.replace("(", "")
        params = params.replace(")", "")
        params = params.split(",")
        int_id = (params[0], params[1], params[2])
        harbor = params[3]
        settlement = eval(params[4])
        city = eval(params[5])
        val.append(Intersection(int_id, harbor, settlement, city))
    if ret_val:
        return val
    bored.__setattr__(attr, val)


def eval_intersections(bored, attr, s):
    val = {}
    s = s.strip("{()}")
    s = s.split("), (")
    for params in s:
        params = params.split(": ")
        tup = eval("(" + params[0])
        intersect_obj = eval_intersection_objects(bored, attr, params[1] + ")", ret_val=True)
        val[tup] = intersect_obj
    bored.__setattr__(attr, val)


if __name__ == "__main__":

    g = Game()
    # g.play(2)
    p = Player(0)
    p1 = Player(1)
    g.player_list[0] = p
    g.player_list[1] = p1
    g.check_longest_road(0)
    # GameEncoder().encode(g)
    x = g.board.__repr__()
    print(x)
    x = str(x)
    board_dict = eval(x)

    mode = board_dict['mode']
    b = Board(mode)
    del board_dict['mode']

    Wood = "Wood"
    Clay = "Clay"
    Sheep = "Sheep"
    Wheat = "Wheat"
    Ore = "Ore"
    Desert = "Desert"
    Ocean = "Ocean"

    # TODO: didn't eval 'edge_objects' key correctly
    for k, v in board_dict.items():
        if k == 'intersection_objects':
            eval_intersection_objects(b, k, v)
        elif k == "intersections":
            eval_intersections(b, k, v)
        else:
            b.__setattr__(k, eval(v))
    b.distribution = np.array(b.distribution)

    print(b.__repr__())

    # print(json.dumps(g, cls=GameEncoder))
"""    
    import sys
    f1 = sys.stdin
    f = open("catan/input.txt", 'r')
    sys.stdin = f
    f.close()
    sys.stdin = f1

    p = Player(0)
    p1 = Player(1)
    g.player_list[0] = p
    g.player_list[1] = p1

    p.backpack.resource_cards["Wood"] = 0
    p.backpack.resource_cards["Clay"] = 0
    p.backpack.resource_cards["Wheat"] = 0
    p.backpack.resource_cards["Sheep"] = 0
    p.backpack.resource_cards["Ore"] = 0
    p1.backpack.resource_cards["Wood"] = 1
    p1.backpack.resource_cards["Clay"] = 2
    p1.backpack.resource_cards["Wheat"] = 5
    p1.backpack.resource_cards["Sheep"] = 4
    p1.backpack.resource_cards["Ore"] = 3
    # g.steal(0, 1)
    # g.buy_dev_card(1)
    # p1.backpack.dev_cards[0].can_use = True
    # g.use_dev_card(1, "knight")
    # g.ux(1, "build settlement")
    # g.build_settlement(1, (-11, -2, 0))
    # g.build_city(0, (-11, -2, 0))
    
    print(g.game_resources)
    print("P0: %s " % p.backpack)
    print("P1: %s" % p1.backpack)
"""
