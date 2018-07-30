from card import *
from constants import *
from hand import *

class Actor(object):
  """
  Base class for interacting with the environment. Allows humans or AIs to use
  the same API.
  """
  def __init__(self, chip_count):
    self.chip_count = chip_count
    self.hands = [Hand()]
    self.hand_count = 0
    self.bet = 0

  def process_state(self, state):
    """
    Processes the incoming state, and returns an action to perform.
    state : dictionary
      - The incoming state. This could be the dealer's card, count, or current
        hand.
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

  def split_hand(self, hand_idx=0):
    """
    Splits a hand into two hands. This is done in place, so the new hand is
    added to the index after the current index.
    hand_idx Int:
      - The index of the hand to split.
    """
    first_card = self.hands[hand_idx].cards[0]
    second_card = self.hands[hand_idx].cards[1]
    self.hands.insert(hand_idx + 1, Hand())
    self.hands[hand_idx].reset()
    self.add_card(first_card, hand_idx)
    self.add_card(second_card, hand_idx + 1)

    self.hands[hand_idx].is_split = True
    self.hands[hand_idx + 1].is_split = True

  def add_card(self, card, hand_idx=0):
    """Add the new card to the player's hand at a given index."""
    self.hands[hand_idx].add_card(card)

  def reset_hand(self):
    """Removes all of the cards from the current hand."""
    self.hands = [Hand()]

  def is_soft_hand(self, hand_idx=0):
    """
    Returns whether the current hand is a soft hand. A soft hand is defined as
    having two cards, summing less than 21, where at least one card is an ace.
    ex) A 6 = 7 or 17. A 10 = 21, and sums to blackjack. This is technically not
    a soft hand. A 6 2 = 20 is not a soft hand because it has more than 2 cards.
    """
    return self.hands[hand_idx].is_soft_hand()

  def count(self, hand_idx=0):
    """
    Returns the max count of the hand. This accounts for the value of an ace.
    """
    return self.hands[hand_idx].count()

  def is_blackjack(self, hand_idx=0):
    """Returns whether a player's hand is a blackjack at a given index."""
    return self.hands[hand_idx].is_blackjack()

  def drawn_cards(self):
    """Returns how many cards the player has drawn."""
    drawn_cards = 0
    for hand in self.hands:
      drawn_cards += len(hand.cards) - 2
    return drawn_cards

  def __str__(self):
    """ex) K 6 - 16"""
    desc = ''
    if len(self.hands) > 1:
      for idx, hand in enumerate(self.hands):
        desc += '(' + str(idx) + ') ' + str(hand) + '\n'
    else:
      desc = str(self.hands[0])

    return desc

  def __repr__(self):
    return self.__str__()
