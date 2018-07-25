from card import *
from player import *

class Dealer(Player):
  def __init__(self, chip_count):
    super().__init__(chip_count)
    self.show_hand = False

  def count(self):
    if self.show_hand:
      return super.count()
    return self.cards[0].max_val

  def __str__(self):
    if self.show_hand:
      return super.__str__()
    return str(self.cards[0]) + str(self.cards[0].max_val)
