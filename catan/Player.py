from catan.Inventory import *
from Catan.Game import *

class Player:

    def __init__(self, player_id, knights_played=0):
        self.player_id = player_id
        self.knights_played = knights_played
        self.backpack = Backpack(5, 4, 16)

    def action(self, input_string):
        if input_string == "build road":

            Game.build_road(self.player_id)            

