import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../..")

import unittest
import src.blackjack as bj

class DealerTestCase(unittest.TestCase):
  def test_obfuscate_count(self):
    dealer = bj.DealerActor()
    dealer.add_card(bj.create_card(10))
    dealer.add_card(bj.create_card(8))

    self.assertEqual(dealer.count(), 10)
    self.assertEqual(str(dealer), '10 X - 10')

    dealer.show_hand = True

    self.assertEqual(dealer.count(), 18)
    self.assertEqual(str(dealer), '10 8 - 18')

  def test_process_state_hit(self):
    dealer = bj.DealerActor()
    dealer.add_card(bj.create_card(5))
    dealer.add_card(bj.create_card(4))

    a = dealer.process_state({})
    self.assertEqual(a, bj.Action.HIT)

  def test_process_state_stand(self):
    dealer = bj.DealerActor()
    dealer.add_card(bj.create_card(10))
    dealer.add_card(bj.create_card(8))

    a = dealer.process_state({})
    self.assertEqual(a, bj.Action.STAND)

  def test_process_state_hard_17(self):
    dealer = bj.DealerActor()
    dealer.add_card(bj.create_card(10))
    dealer.add_card(bj.create_card(7))

    a = dealer.process_state({})
    self.assertEqual(a, bj.Action.STAND)

  def test_process_state_soft_17(self):
    dealer = bj.DealerActor()
    dealer.add_card(bj.create_ace())
    dealer.add_card(bj.create_card(6))

    a = dealer.process_state({})
    self.assertEqual(a, bj.Action.HIT)

  def test_process_state_stand_17(self):
    dealer = bj.DealerActor()
    dealer.add_card(bj.create_ace())
    dealer.add_card(bj.create_card(3))
    dealer.add_card(bj.create_card(3))

    a = dealer.process_state({})
    self.assertEqual(a, bj.Action.STAND)

  def test_process_state_soft_18(self):
    dealer = bj.DealerActor()
    dealer.add_card(bj.create_ace())
    dealer.add_card(bj.create_card(8))

    a = dealer.process_state({})
    self.assertEqual(a, bj.Action.STAND)


if __name__ == '__main__':
  unittest.main()
