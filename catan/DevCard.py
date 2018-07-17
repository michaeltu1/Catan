class DevCard:
    """
    Needed to keep track of when a player can use their dev card
    """
    def __init__(self, card_type, description, turn_bought=0, used=False):
        self.card_type = card_type
        self.description = description
        self.turn_bought = turn_bought
        self.used = used

    def __str__(self):
        return "Card type: %s, Description: %s, Turn bought: %s, Used: %s" % \
               (self.card_type, self.description, self.turn_bought, self.used)

    def __repr__(self):
        return "DevCard(%s, %s, %s, %s)" % (self.card_type, self.description, self.turn_bought, self.used)
