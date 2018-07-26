import functools
import random
from card import *

class Shoe(object):
  """Represents the shoe where all of the cards are stored."""
  def __init__(self, shoe_size, reshuffle_ratio):
    self._cards = self._create_shoe(shoe_size)
    self.reshuffle_ratio = reshuffle_ratio
    self._idx = 0
    self._hilo_count = 0
    self.shuffle()

  def shuffle(self):
    """Shuffles the cards and sets the current index back to 0."""
    random.shuffle(self._cards)
    self._idx = 0

  def depth(self):
    """Returns the percent of the shoe that has been used."""
    return self._idx / len(self._cards)

  def draw(self):
    """
    Draws and returns the top card from the shoe. If the shoe is empty it will
    reshuffle the shoe. Reshuffling will not happen if the reshuffle ratio is
    met. This is to ensure a hand is played without destroying the current
    count.
    """
    card = self._cards[self._idx]
    self._idx += 1
    self._hilo_count += card.hilo_count()

    if self._idx == len(self._cards):
      self.shuffle()
    return card

  def peek(self, length):
    """Returns the top-N cards. This does not change the current index."""
    return self._cards[self._idx:min(len(self._cards), self._idx + length)]

  def hilo_count(self):
    """Returns the hi-lo count of the shoe."""
    return self._hilo_count

  def _create_shoe(self, shoe_size):
    """
    Creates the shoe by appending 4x the number of allotted decks. This is to
    account for different suits.
    """
    cards = []
    for i in range(4 * shoe_size):
      cards.append(Card(1, 11, 'A'))
      cards.append(Card(10, 10, 'K'))
      cards.append(Card(10, 10, 'Q'))
      cards.append(Card(10, 10, 'J'))
      cards.append(Card(10, 10, '10'))
      cards.append(Card(9, 9, '9'))
      cards.append(Card(8, 8, '8'))
      cards.append(Card(7, 7, '7'))
      cards.append(Card(6, 6, '6'))
      cards.append(Card(5, 5, '5'))
      cards.append(Card(4, 4, '4'))
      cards.append(Card(3, 3, '3'))
      cards.append(Card(2, 2, '2'))
    return cards
