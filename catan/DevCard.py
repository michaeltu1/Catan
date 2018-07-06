class DevCard:
    """
    Needed to keep track of when a player can use their dev card
    """
    def __init__(self, card_type, description, can_use=False, used=False):
        self.card_type = card_type
        self.description = description
        self.can_use = can_use
        self.used = used

    def __str__(self):
        return "Card type: %s, Description: %s, Can_use: %s, Used: %s" % \
               (self.card_type, self.description, self.can_use, self.used)

    def __repr__(self):
        return "DevCard(%s, %s, %s, %s)" % (self.card_type, self.description, self.can_use, self.used)