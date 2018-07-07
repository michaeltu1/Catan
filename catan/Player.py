from catan.Inventory import *
# Maybe don't need to import everything


class Player:
    # Turns start when the dice is rolled
    def __init__(self, player_id, turn_number=1, knights_played=0, dev_cards_used=False):
        self.player_id = player_id
        self.turn_number = turn_number
        self.knights_played = knights_played
        self.dev_cards_used = dev_cards_used
        self.backpack = Backpack(5, 4, 16)
    
    def __str__(self):
        return "Player id: %s, Turn number: %s, knights played: %s, backpack: %s" % \
                (self.player_id, self.turn_number, self.knights_played, self.backpack)

    def __repr__(self):
        return "Player(%s, %s, %s, %s)" % (self.player_id, self.turn_number, self.knights_played, self.backpack)
