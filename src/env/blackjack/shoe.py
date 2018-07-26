import functools
import random
from card import *

class Shoe(object):
  def __init__(self, shoe_size, reshuffle_ratio):
    self._cards = self._create_shoe(shoe_size)
    self.reshuffle_ratio = reshuffle_ratio
    self._idx = 0
    self._hilo_count = 0
    self.shuffle()

  def shuffle(self):
    random.shuffle(self._cards)
    self._idx = 0

  def depth(self):
    return self._idx / len(self._cards)

  def draw(self):
    card = self._cards[self._idx]
    self._idx += 1
    self._hilo_count += card.hilo_count()

    if self._idx == len(self._cards):
      self.shuffle()
    return card

  def peek(self, length):
    return self._cards[self._idx:min(len(self._cards), self._idx + length)]

  def hilo_count(self):
    return self._hilo_count

  def _create_shoe(self, shoe_size):
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
