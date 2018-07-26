from actor import *

class HumanActor(Actor):
  """An actor that is controlled via a CLI and played by a human."""
  def __init__(self, chip_count):
    super().__init__(chip_count)
    self.bet = 10

  def process_state(self, state):
    super().process_state(state)
    a = input('Choose your action. Count: ' + str(state['count']) + '\nHit (h), Stand (s), Double (d):\t')
    if a == 'h' or a == 'H':
      return HIT
    elif a == 's' or a == 'S':
      return STAND
    elif a == 'd' or a == 'D':
      return DOUBLE_DOWN

    return STAND
