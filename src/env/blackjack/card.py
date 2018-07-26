class Card(object):
  """
  Representation of a single card. Since blackjack is suit agnostic, suits are
  not represented.
  """
  def __init__(self, min_val, max_val, desc):
    self.min_val = min_val
    self.max_val = max_val
    self.desc = desc

  def hilo_count(self):
    """
    Returns the hi lo count of the card.
    10 and up has a value of -1.
    7-9 has a value of 0.
    6 and below has a value of +1.
    """
    if self.max_val > 9:
      return -1
    elif self.max_val < 7:
      return 1
    else:
      return 0

  def is_ace(self):
    """Returns whether the card is an ace or not."""
    return self.desc == 'A'

  def __str__(self):
    return self.desc
  def __repr__(self):
    return self.__str__()
