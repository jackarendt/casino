from actor import *
from player import *

class DealerActor(Actor):
  def process_state(self, state):
    self.player.show_hand = True
    count = self.player.count()

    if count < 17:
      return DRAW
    if count == 17 and self.player.is_soft_hand():
      return DRAW
    return STAND
