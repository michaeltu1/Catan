

# originally in intersection but moved to here
def build(self):
    if self.intersect_ID not in Game.unbuildable:
        Game.unbuildable.add(self.intersect_ID)
        Game.unbuildable.add((self.intersect_ID.index(0) + 20,
                              self.intersect_ID.index(1), self.intersect_ID.index(2)))
        Game.unbuildable.add((self.intersect_ID.index(0),
                              self.intersect_ID.index(1) - 7, self.intersect_ID.index(2)))
        Game.unbuildable.add((self.intersect_ID.index(0),
                              self.intersect_ID.index(1), self.intersect_ID.index(2) - 13))
