import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
import src.blackjack as bj

class HandTestCase(unittest.TestCase):
  def test_basic_hand(self):
    hand = bj.Hand()
    hand.add_card(bj.create_card(10))
    hand.add_card(bj.create_card(8))

    self.assertEqual(hand.count(), 18)
    self.assertFalse(hand.is_blackjack())
    self.assertTrue(hand.can_double_down())
    self.assertFalse(hand.can_split())
    self.assertFalse(hand.is_soft_hand())

  def test_count_append(self):
    hand = bj.Hand()
    hand.add_card(bj.create_ace())
    hand.add_card(bj.create_card(5))
    self.assertEqual(hand.count(), 16)

    hand.add_card(bj.create_card(4))
    self.assertEqual(hand.count(), 20)

    hand.add_card(bj.create_card(8))
    self.assertEqual(hand.count(), 18)

    hand.add_card(bj.create_card(5))
    self.assertEqual(hand.count(), 23)

  def test_reset(self):
    hand = bj.Hand()
    hand.add_card(bj.create_card(8))
    hand.add_card(bj.create_card(8))
    hand.reset()

    self.assertEqual(len(hand.cards), 0)

  def test_aces(self):
    hand = bj.Hand()
    hand.add_card(bj.create_ace())
    hand.add_card(bj.create_card(8))

    self.assertTrue(hand.is_soft_hand())

    hand.add_card(bj.create_ace())
    self.assertEqual(hand.count(), 20)

    hand.add_card(bj.create_card(10))
    self.assertEqual(hand.count(), 20)

  def test_split(self):
    hand = bj.Hand()
    hand.add_card(bj.create_card(8))
    hand.add_card(bj.create_card(8))

    self.assertTrue(hand.can_split())

  def test_is_blackjack(self):
    hand = bj.Hand()
    hand.add_card(bj.create_card(10))
    hand.add_card(bj.create_ace())

    self.assertTrue(hand.is_blackjack())

    hand.add_card(bj.create_card(10))
    self.assertEqual(hand.count(), 21)
    self.assertFalse(hand.is_blackjack())

if __name__ == '__main__':
  unittest.main()
