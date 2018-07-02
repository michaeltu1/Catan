from catan.Inventory import *

# originally in intersection but moved to here
# need to update board or game with updated intersection attributes (has_settlement or has_city)
def build_settlement(self, intersect_id):
    if intersect_id not in Game.unbuildable:
        Game.unbuildable.add(intersect_id)
        Game.unbuildable.add((intersect_id.index(0) + 20,
                              intersect_id.index(1), intersect_id.index(2)))
        Game.unbuildable.add((intersect_id.index(0),
                              intersect_id.index(1) - 7, intersect_id.index(2)))
        Game.unbuildable.add((intersect_id.index(0),
                              intersect_id.index(1), intersect_id.index(2) - 13))
        # TODO: somehow reach intersection object from intersect ID
        "???".has_settlement = True
        # check longest road

class Player:

    def __init__(self, player_id, knights_played=0):
        self.player_id = player_id
        self.knights_played = knights_played
        self.backpack = Backpack(5, 4, 16)

    def action(self, input_string):
        if input_string == "build road":


