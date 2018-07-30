from actor import *
from constants import *

class HumanActor(Actor):
  """An actor that is controlled via a CLI and played by a human."""
  def __init__(self, chip_count):
    super().__init__(chip_count)
    self.bet = 10

  def process_state(self, state):
    super().process_state(state)

    can_double = state.get(DOUBLE_DOWN_STATE_KEY)
    can_split = state.get(SPLIT_STATE_KEY)
    insurance = state.get(INSURANCE_STATE_KEY)

    if insurance:
      a = input('Take Insurance? (y/n):  ')
      return self._process_input(a, False, False, insurance)

    input_str = 'Hit (h), Stand (s)'
    if can_double:
      input_str += ', Double down (d)'
    if can_split:
      input_str += ', Split (l)'

    a = input('Choose your action. Count: ' + str(state.get(COUNT_STATE_KEY)) +
              '\n' + input_str + ':  ')

    return self._process_input(a, can_double, can_split, insurance)

  def _process_input(self, a, can_double, can_split, insurance):
    if (a == 'h' or a == 'H') and not insurance:
      return Action.HIT
    elif a == 's' or a == 'S':
      return Action.STAND
    elif (a == 'd' or a == 'D') and can_double:
      return Action.DOUBLE_DOWN
    elif (a == 'l' or a == 'L') and can_split:
      return Action.SPLIT
    elif (a == 'y' or a == 'Y') and insurance:
      return Action.INSURANCE

    return Action.STAND
