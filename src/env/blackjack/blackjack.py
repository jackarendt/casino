import dealer
import dealer_actor
import human_actor
import player
import shoe

class Blackjack(object):
  def __init__(self, num_agents, print_desc, is_human):
    self.shoe = shoe.Shoe(6, 0.8)
    self.dealer = dealer_actor.DealerActor(dealer.Dealer(1000000))
    self.agents = []

    for i in range(num_agents):
      if is_human:
        agent = human_actor.HumanActor(player.Player(1000))
        self.agents.append(agent)


if __name__ == '__main__':
  print('Welcome to blackjack. Let\'s shuffle up and deal.')
  env = Blackjack(1, True, True)
