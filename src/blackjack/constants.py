from enum import Enum

# The value of blackjack.
BLACKJACK_VALUE = 21
# The value that the dealer has to stay at.
DEALER_STAY_VALUE = 17

class Action(Enum):
  STAND = 0
  HIT = 1
  DOUBLE_DOWN = 2
  SPLIT = 3
  INSURANCE = 4

# State keys for processing state.
DEALER_STATE_KEY = 'dealer'
COUNT_STATE_KEY = 'count'
DOUBLE_DOWN_STATE_KEY = 'double'
SPLIT_STATE_KEY = 'split'
HAND_INDEX_STATE_KEY = 'hand_idx'
INSURANCE_STATE_KEY = 'insurance'
