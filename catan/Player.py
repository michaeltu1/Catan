from catan.Inventory import *
# Maybe don't need to import everything

class Player:
    
    def __init__(self, player_id, knights_played=0):
        self.player_id = player_id
        self.knights_played = knights_played
        self.backpack = Backpack(5, 4, 16)

