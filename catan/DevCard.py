class DevCard:
    """
    Needed to keep track of when a player can use their dev card
    """
    def __init__(self, card_type, description, turn_bought=0, used=False):
        self.card_type = card_type
        self.description = description
        self.turn_bought = turn_bought
        self.used = used

    @staticmethod
    def craft(desc, num):
        make = {"Knight": lambda: DevCard("Knight", "Can be used to move the robber"),
                "Victory Point": lambda: DevCard("Victory Point", "Gives the player 1 Victory Point"),
                "Road Building": lambda: DevCard("Road Building", "Allows the player to place 2 roads"),
                "Year of Plenty": lambda: DevCard("Year of Plenty", "Draw any 2 resource from bank"),
                "Monopoly": lambda: DevCard("Monopoly", "Claim all resource cards of a specified type")}
        return [make[desc] for _ in range(num)]

    def __str__(self):
        return "Card type: %s, Description: %s, Turn bought: %s, Used: %s" % \
               (self.card_type, self.description, self.turn_bought, self.used)

    def __repr__(self):
        return "DevCard(%s, %s, %s, %s)" % (self.card_type, self.description, self.turn_bought, self.used)
