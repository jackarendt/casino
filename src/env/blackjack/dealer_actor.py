from actor import *

class DealerActor(Actor):
  """
  An actor that represents how a dealer behaves on the table. It follows Vegas
  rules. Hit on soft 17.
  """
  def __init__(self, chip_count):
    super().__init__(chip_count)
    self.show_hand = False

  def process_state(self, state):
    super().process_state(state)
    self.show_hand = True
    count = self.count()

    # The dealer should hit on 17 or below, or on soft 17.
    if count <= 17 or (count == 17 and self.is_soft_hand()):
      return HIT
    return STAND

  def process_reward(self, chip_reward, other_reward):
    super().process_reward(chip_reward, other_reward)
    self.show_hand = False

  def count(self):
    # Return the full count if the dealer should show their hand. Otherwise only
    # return the max value of the first card.
    if self.show_hand:
      return super().count()
    return self.cards[0].max_val

  def __str__(self):
    # Return the description for all of the cards if the dealer should show
    # their hand. Otherwise obfuscate the second card.
    if self.show_hand:
      return super().__str__()
    return str(self.cards[0]) + ' X - ' + str(self.cards[0].max_val)
