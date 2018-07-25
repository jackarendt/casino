from player import *

STAND = 0
DRAW = 1
DOUBLE = 2
SPLIT = 3

class Actor(object):
  def __init__(self, player):
    self.player = player


  def process_state(self, state):
    pass

  def process_reward(self, chip_reward, other_reward):
    self.player.chip_count += chip_reward
