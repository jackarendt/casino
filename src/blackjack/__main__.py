from blackjack.game import Blackjack
from blackjack.human_actor import HumanActor

if __name__ == '__main__':
  print('Welcome to blackjack. Let\'s shuffle up and deal.')
  env = Blackjack([HumanActor(1000)], True)
  for i in range(10):
    env.deal()
    env.play()
    env.assess_rewards()

  print('END: ' + str(env.agents[0].chip_count))
