import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
import src.blackjack as bj

class ActorTestCase(unittest.TestCase):
  def test_count(self):
    actor = bj.Actor()
    actor.add_card(bj.create_card(10))
    actor.add_card(bj.create_card(8))
    self.assertEqual(actor.count(), 18)

  def test_count_multiple_hands(self):
    actor = bj.Actor()
    actor.add_card(bj.create_card(10))
    actor.add_card(bj.create_card(8))

    # Add a new hand.
    actor.hands.append(bj.Hand())
    actor.add_card(bj.create_card(6), 1)
    actor.add_card(bj.create_card(5), 1)

    self.assertEqual(actor.count(), 18)
    self.assertEqual(actor.count(1), 11)

  def test_process_reward(self):
    actor = bj.Actor(100)
    actor.process_reward(10, 0)
    self.assertEqual(actor.chip_count, 110)

    self.assertEqual(len(actor.hands), 1)
    self.assertEqual(len(actor.hands[0].cards), 0)

  def test_drawn_cards(self):
    actor = bj.Actor()
    actor.add_card(bj.create_card(3))
    actor.add_card(bj.create_card(2))
    actor.add_card(bj.create_card(5))
    actor.add_card(bj.create_card(6))
    actor.add_card(bj.create_card(3))

    self.assertEqual(actor.drawn_cards(), 3)

  def test_drawn_cards_multiple_hands(self):
    actor = bj.Actor()
    actor.add_card(bj.create_card(3))
    actor.add_card(bj.create_card(5))

    actor.hands.append(bj.Hand())
    actor.add_card(bj.create_card(6), 1)
    actor.add_card(bj.create_card(5), 1)
    actor.add_card(bj.create_card(6), 1)

    actor.hands.append(bj.Hand())
    actor.add_card(bj.create_card(3), 2)
    actor.add_card(bj.create_card(8), 2)
    actor.add_card(bj.create_card(5), 2)

    self.assertEqual(actor.drawn_cards(), 2)

  def test_drawn_cards_multiple_hands_no_cards(self):
    actor = bj.Actor()
    actor.add_card(bj.create_card(3))
    actor.add_card(bj.create_card(5))

    actor.hands.append(bj.Hand())
    actor.add_card(bj.create_card(6), 1)
    actor.add_card(bj.create_card(5), 1)

    actor.hands.append(bj.Hand())
    actor.add_card(bj.create_card(3), 2)
    actor.add_card(bj.create_card(8), 2)

    self.assertEqual(actor.drawn_cards(), 0)

  def test_string(self):
    actor = bj.Actor()
    actor.add_card(bj.create_card(10))
    actor.add_card(bj.create_card(6))

    self.assertEqual(str(actor), '10 6 - 16')

  def test_string_multiple_hands(self):
    actor = bj.Actor()
    actor.add_card(bj.create_card(3))
    actor.add_card(bj.create_card(5))

    actor.hands.append(bj.Hand())
    actor.add_card(bj.create_card(6), 1)
    actor.add_card(bj.create_card(5), 1)

    self.assertEqual(str(actor), '(0) 3 5 - 8\n(1) 6 5 - 11\n')

  def test_split_single_hand(self):
    actor = bj.Actor()
    actor.add_card(bj.create_card(5))
    actor.add_card(bj.create_card(5))

    actor.split_hand()

    self.assertEqual(len(actor.hands), 2)
    self.assertEqual(actor.count(), 5)
    self.assertEqual(actor.hands[0].cards[0].min_val, 5)
    self.assertTrue(actor.hands[0].is_split)

    self.assertEqual(actor.count(1), 5)
    self.assertEqual(actor.hands[1].cards[0].min_val, 5)
    self.assertTrue(actor.hands[1].is_split)

  def test_split_multiple_hands(self):
    actor = bj.Actor()
    actor.add_card(bj.create_card(5))
    actor.add_card(bj.create_card(5))

    actor.hands.append(bj.Hand())
    actor.add_card(bj.create_card(8), 1)
    actor.add_card(bj.create_card(7), 1)

    actor.split_hand()

    self.assertEqual(len(actor.hands), 3)
    self.assertEqual(actor.count(), 5)
    self.assertEqual(actor.hands[0].cards[0].min_val, 5)
    self.assertTrue(actor.hands[0].is_split)

    self.assertEqual(actor.count(1), 5)
    self.assertEqual(actor.hands[1].cards[0].min_val, 5)
    self.assertTrue(actor.hands[1].is_split)

    self.assertEqual(actor.hands[2].cards[0].min_val, 8)

if __name__ == '__main__':
  unittest.main()
