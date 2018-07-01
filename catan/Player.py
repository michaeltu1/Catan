from catan.Inventory import *

# originally in intersection but moved to here
# need to update board or game with updated intersection attributes (has_settlement or has_city)
def build_settlement(self):
    if self.intersect_ID not in Game.unbuildable:
        Game.unbuildable.add(self.intersect_ID)
        Game.unbuildable.add((self.intersect_ID.index(0) + 20,
                              self.intersect_ID.index(1), self.intersect_ID.index(2)))
        Game.unbuildable.add((self.intersect_ID.index(0),
                              self.intersect_ID.index(1) - 7, self.intersect_ID.index(2)))
        Game.unbuildable.add((self.intersect_ID.index(0),
                              self.intersect_ID.index(1), self.intersect_ID.index(2) - 13))

class Player:

    def __init__(self, player_id, knights_played=0):
        self.player_id = player_id
        self.knights_played = knights_played
        self.backpack = Backpack(5, 4, 16)

    def action(self, input_string):
        if input_string == "build road":


