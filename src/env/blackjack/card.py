class Card(object):
  def __init__(self, min_val, max_val, desc):
    self.min_val = min_val
    self.max_val = max_val
    self.desc = desc

  def hilo_count(self):
    if self.max_val > 9:
      return -1
    elif self.max_val < 7:
      return 1
    else:
      return 0

  def __str__(self):
    return self.desc
  def __repr__(self):
    return self.desc
