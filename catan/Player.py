from catan.Inventory import Backpack


class Player:
    def __init__(self, player_id, turn_number=1, knights_played=0, dev_cards_used=False, road_length=0):
        self.player_id = player_id
        self.turn_number = turn_number
        self.knights_played = knights_played
        self.dev_cards_used = dev_cards_used
        self.road_length = road_length
        self.backpack = Backpack(5, 4, 16)
    
    def __str__(self):
        return "Player id: %s, Turn number: %s, knights played: %s, backpack: %s" % \
                (self.player_id, self.turn_number, self.knights_played, self.backpack)

    def __repr__(self):
        return "Player(%s, %s, %s, %s)" % (self.player_id, self.turn_number, self.knights_played, self.backpack)
