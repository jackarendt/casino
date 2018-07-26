import actor
import dealer_actor
import human_actor
import shoe

class Blackjack(object):
  """
  An environment focused on playing blackjack. Can be played by a human or agent. Agents should
  override `Actor` to provide custom functionality based on the current state. An advantage of using
  this environment is that it allows for many actors to play at once and accumulate different
  experiences.
  """
  def __init__(self, num_agents, print_desc, is_human):
    self.shoe = shoe.Shoe(6, 0.8)
    self.dealer = dealer_actor.DealerActor(1000000)
    self.agents = []
    self.player_count = num_agents + 1
    self.print_desc = print_desc

    for i in range(num_agents):
      if is_human:
        agent = human_actor.HumanActor(1000)
        self.agents.append(agent)

  def deal(self):
    if self.shoe.depth() > self.shoe.reshuffle_ratio:
      self.shoe.shuffle()

    for i in range(2 * self.player_count):
      card = self.shoe.draw()
      if i % self.player_count == self.player_count - 1:
        self.dealer.cards.append(card)
      else:
        self.agents[i % self.player_count].cards.append(card)

    if self.print_desc:
      print('Dealer: ' + str(self.dealer))
      for idx, agent in enumerate(self.agents):
        print('Player ' + str(idx + 1) + ': ' + str(agent))
      print('-------------------------')

  def play(self):

    for idx, agent in enumerate(self.agents):
      state = {
        'state': self.dealer.cards[0],
        'count': self.shoe.hilo_count()
      }

      d = False
      while not d:
        if agent.count() > 21:
          break

        a = agent.process_state(state)
        if self.print_desc:
          print('Player ' + str(idx + 1) + ': ' + str(agent))
        if a == actor.HIT or actor.DOUBLE_DOWN:
          state['new_card'] = self.shoe.draw()
        d = a == actor.STAND or a == actor.DOUBLE_DOWN

      if self.print_desc:
        print('[FINAL] Player ' + str(idx + 1) + ': ' + str(agent))

    d = False
    self.dealer.show_hand = True

    state = {}
    while not d:
      if self.dealer.count() > 21:
        break

      a = self.dealer.process_state(state)
      if self.print_desc:
        print('Dealer: ' + str(self.dealer))
      if a == actor.HIT:
        state['new_card'] = self.shoe.draw()
      d = a == actor.STAND

    if self.print_desc:
      print('[FINAL] Dealer: ' + str(self.dealer))
      print('-------------------------')

  def assess_rewards(self):
    dealer_count = self.dealer.count()
    dealer_bust = dealer_count > 21
    self.dealer.process_reward(0, 0)

    for idx, agent in enumerate(self.agents):
      additional_cards = len(agent.cards) - 2
      player_count = agent.count()
      if player_count > 21:
        agent.process_reward(-1 * agent.bet, additional_cards)
        self._print_reward(idx, False, False, -1 * agent.bet)
      elif dealer_bust or player_count > dealer_count:
        blackjack = agent.count() == 21 and len(agent.cards) == 2
        multiplier = 1.5 if blackjack else 1
        agent.process_reward(multiplier * agent.bet, additional_cards)
        self._print_reward(idx, True, False, multiplier * agent.bet)
      elif dealer_count == agent:
        agent.process_reward(0, additional_cards)
        self._print_reward(idx, False, True, 0)
      else:
        agent.process_reward(-1 * agent.bet, additional_cards)
        self._print_reward(idx, False, False, -1 * agent.bet)

      if self.print_desc:
        print('\n\n')

  def _print_reward(self, agent_idx, won, draw, reward):
    if not self.print_desc:
      return

    if won:
      print('Player ' + str(agent_idx + 1) + ' won. +' + str(reward))
    elif draw:
      print('Player ' + str(agent_idx + 1) + ' pushed.')
    else:
      print('Player ' + str(agent_idx + 1) + ' lost. ' + str(reward))

if __name__ == '__main__':
  print('Welcome to blackjack. Let\'s shuffle up and deal.')
  env = Blackjack(1, True, True)
  for i in range(2):
    env.deal()
    env.play()
    env.assess_rewards()
