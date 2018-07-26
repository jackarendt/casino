from actor import *
from player import *

class HumanActor(Actor):
  def __init__(self, chip_count):
    super().__init__(chip_count)
    self.bet = 10

  def process_state(self, state):
    super().process_state(state)
    return STAND
