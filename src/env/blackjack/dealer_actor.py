from actor import *
from player import *

class DealerActor(Actor):
  def process_state(self, state):
    super().process_state(state)
    self.player.show_hand = True
    count = self.player.count()

    if count < 17:
      return HIT
    if count == 17 and self.player.is_soft_hand() and len(self.player.cards) == 2:
      return HIT
    return STAND

  def process_reward(self, chip_reward, other_reward):
    super().process_reward(chip_reward, other_reward)
    self.player.show_hand = False
