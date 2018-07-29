from blackjack.game import Blackjack

if __name__ == '__main__':
  print('Welcome to blackjack. Let\'s shuffle up and deal.')
  env = Blackjack(1, True, True)
  for i in range(20):
    env.deal()
    env.play()
    env.assess_rewards()
