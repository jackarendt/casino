from actor import *
from player import *

class HumanActor(Actor):
  def __init__(self, player):
    super().__init__(player)
    self.bet = 10

  def process_state(self, state):
    super().process_state(state)
    return STAND
