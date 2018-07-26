from card import *

STAND = 0
HIT = 1
DOUBLE_DOWN = 2
SPLIT = 3

class Actor(object):
  """
  Base class for interacting with the environment. Allows humans or AIs to use
  the same API.
  """
  def __init__(self, chip_count):
    self.chip_count = chip_count
    self.cards = []
    self.bet = 0

  def process_state(self, state):
    """
    Processes the incoming state, and returns an action to perform.
    state : dictionary
      - The incoming state. This could be the dealer's card, count, or the
        recently drawn card.
    returns : int
    """
    pass

  def process_reward(self, chip_reward, other_reward):
    """
    Processes the reward at the end of the hand.
    chip_reward : int
      - The chip reward that is returned. i.e. The amount of money the user
        won/lost.
    other_reward : int
      - Any other reward that is returned at the end of a hand. This could be
        used to influence how an agent performs.
    """

    # Add the new chip reward and reset the hand.
    self.chip_count += chip_reward
    self.reset_hand()

  def add_card(self, card):
    # Add the new card to the player's hand.
    self.cards.append(card)

  def reset_hand(self):
    """Removes all of the cards from the current hand."""
    self.cards = []

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
    if filter(lambda card: card.is_ace(), self.cards) is not None:
      return True

    # Sum all of the min values in the hand. If the sum comes to less than 11,
    # then it means that there is room for an ace to take on the value of 11 or
    # 1.
    total = 0
    for card in self.cards:
      total += card.min_value

    return card.min_value < 11

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
      if card.is_ace() and total + card.max_val > 21:
        total += card.min_val
      else:
        total += card.max_val

    return total

  def __str__(self):
    """ex) K 6 - 16"""
    desc = ''
    for card in self.cards:
      desc += str(card) + ' '

    desc += '- ' + str(self.count())
    return desc

  def __repr__(self):
    return self.__str__()
