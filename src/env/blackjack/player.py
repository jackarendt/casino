from card import *

class Player(object):
  def __init__(self, chip_count):
    self.chip_count = chip_count
    self.cards = []

  def reset_hand(self):
    self.cards = []

  def is_soft_hand(self):
    if filter(lambda card: card.desc == 'A', self.cards) is not None:
      return True

    total = 0
    for card in self.cards:
      total += card.min_value

    return card.min_value < 11

  def count(self):
    total = 0
    has_ace = False
    for card in self.cards:
      if card.desc == 'A':
        has_ace = True
      total += card.max_val

    if has_ace and total > 21:
      total -= 10

    return total

  def __str__(self):
    desc = ''
    for card in self.cards:
      desc += str(card) + ' '

    desc += '- ' + str(self.count())
    return desc

  def __repr__(self):
    return self.__str__()
