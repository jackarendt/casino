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
    # Add the new card to the player's hand.
    new_card = state.get('new_card')
    if new_card is not None:
      self.cards.append(new_card)
      state['new_card'] = None

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
