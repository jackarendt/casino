from card import *
from constants import *

class Hand(object):
  """A class that represents the behavior of a player's hand."""
  def __init__(self):
    self.cards = []
    self.is_split = False
    self.did_double = False

  def is_soft_hand(self):
    """
    Returns whether the current hand is a soft hand. A soft hand is defined as
    having two cards, summing less than 21, where at least one card is an ace.
    ex) A 6 = 7 or 17. A 10 = 21, and sums to blackjack. This is technically not
    a soft hand. A 6 2 = 20 is not a soft hand because it has more than 2 cards.
    """
    if len(self.cards) != 2:
      return False

    # Check if the user has an ace.
    if filter(lambda card: card.is_ace(), self.cards) is None:
      return False

    # Sum all of the min values in the hand. If the sum comes to less than 11,
    # then it means that there is room for an ace to take on the value of 11 or
    # 1.
    total = 0
    for card in self.cards:
      total += card.min_val

    return total < 11

  def add_card(self, card):
    """Add the new card to the player's hand."""
    self.cards.append(card)

  def reset(self):
    self.cards = []

  def count(self):
    """
    Returns the max count of the hand. This accounts for the value of an ace.
    """
    # Sort the cards by the max_val. This ensures that aces are counted last.
    sorted_cards = sorted(self.cards, key=lambda card: card.max_val)

    total = 0
    for card in sorted_cards:
      # The ace will have a value of 1 if the new total would be greater than
      # 21.
      if card.is_ace() and total + card.max_val > BLACKJACK_VALUE:
        total += card.min_val
      else:
        total += card.max_val

    return total

  def is_blackjack(self):
    """Returns whether the hand is a blackjack or not."""
    return self.count() == BLACKJACK_VALUE and len(self.cards) == 2

  def can_double_down(self):
    """Returns whether the player can double down or not."""
    return len(self.cards) == 2

  def can_split(self):
    """Returns whether the player can split the hand or not."""
    return len(self.cards) == 2 and self.cards[0] == self.cards[1]

  def __str__(self):
    """ex) K 6 - 16"""
    desc = ''
    for card in self.cards:
      desc += str(card) + ' '

    desc += '- ' + str(self.count())
    return desc

  def __repr__(self):
    return self.__str__()
