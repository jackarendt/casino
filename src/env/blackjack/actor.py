from player import *

STAND = 0
HIT = 1
DOUBLE_DOWN = 2
SPLIT = 3

class Actor(object):
  def __init__(self, player):
    self.player = player
    self.bet = 0

  def process_state(self, state):
    new_card = state.get('new_card')
    if new_card is not None:
      self.player.cards.append(new_card)
      state['new_card'] = None

  def process_reward(self, chip_reward, other_reward):
    self.player.chip_count += chip_reward
    self.player.reset_hand()
