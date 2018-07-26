import actor
import dealer_actor
import human_actor
import shoe

BLACKJACK_COUNT = 21

class Blackjack(object):
  """
  An environment focused on playing blackjack. Can be played by a human or
  agent. Agents should override `Actor` to provide custom functionality based on
  the current state. An advantage of using this environment is that it allows
  for many actors to play at once and accumulate different experiences.
  """
  def __init__(self, num_agents, print_desc, is_human):
    # A typical shoe has 6 decks and reshuffles when roughly 5/6 decks are used.
    self.shoe = shoe.Shoe(6, 0.8)
    self.dealer = dealer_actor.DealerActor(1000000)
    self.agents = []
    self.player_count = num_agents + 1
    self.print_desc = print_desc

    # Add the agents.
    for i in range(num_agents):
      if is_human:
        agent = human_actor.HumanActor(1000)
        self.agents.append(agent)

  def deal(self):
    """Deals the cards to the various players and agents."""
    if self.shoe.depth() > self.shoe.reshuffle_ratio:
      self.shoe.shuffle()

    for i in range(2 * self.player_count):
      card = self.shoe.draw()
      # Deal the card to the dealer last. This makes indexing easier, as well as
      # follows Vegas rules.
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
    """
    Iterates through all of the agents and then the dealer to play their hand.
    """
    for idx, agent in enumerate(self.agents):
      d = False
      while not d:
        # The count should be adjusted such that the dealer's second card count
        # isn't revealed.
        state = {
          'state': self.dealer.cards[0],
          'count': self.shoe.hilo_count() - self.dealer.cards[1].hilo_count()
        }

        # Process the current state.
        a = agent.process_state(state)

        # Add the card if the user hit.
        if a == actor.HIT or a == actor.DOUBLE_DOWN:
          agent.add_card(self.shoe.draw())

        # Print the description after the user takes their action.
        if self.print_desc:
          print('Player ' + str(idx + 1) + ': ' + str(agent))

        # The agent is finished after they stand, or double down.
        d = (a == actor.STAND or a == actor.DOUBLE_DOWN or
            agent.count() > BLACKJACK_COUNT)

      if self.print_desc:
        print('[FINAL] Player ' + str(idx + 1) + ': ' + str(agent))

    d = False
    self.dealer.show_hand = True
    if self.print_desc:
      print('Dealer: ' + str(self.dealer))

    while not d:
      a = self.dealer.process_state({})
      if a == actor.HIT:
        self.dealer.add_card(self.shoe.draw())

      if self.print_desc:
        print('Dealer: ' + str(self.dealer))

      # Dealer is done when they stand or bust.
      d = a == actor.STAND or self.dealer.count() >= BLACKJACK_COUNT

    if self.print_desc:
      print('[FINAL] Dealer: ' + str(self.dealer))
      print('-------------------------')

  def assess_rewards(self):
    dealer_count = self.dealer.count()
    dealer_bust = dealer_count > BLACKJACK_COUNT
    self.dealer.process_reward(0, 0)

    for idx, agent in enumerate(self.agents):
      additional_cards = len(agent.cards) - 2
      player_count = agent.count()
      if (player_count > BLACKJACK_COUNT or
        (agent.count() < dealer_count and dealer_count < BLACKJACK_COUNT)):
        # Agent loses if they bust or they score less than the dealer without
        # the dealer busting.
        agent.process_reward(-1 * agent.bet, additional_cards)
        self._print_reward(idx, False, False, -1 * agent.bet)
      elif (dealer_bust or player_count > dealer_count or
          (agent.count() == BLACKJACK_COUNT and len(agent.cards) == 2)):
        # Agent wins if the dealer busts, or they score better than the dealer
        # or the user has blackjack.
        blackjack = agent.count() == BLACKJACK_COUNT and len(agent.cards) == 2
        multiplier = 1.5 if blackjack else 1
        agent.process_reward(multiplier * agent.bet, additional_cards)
        self._print_reward(idx, True, False, multiplier * agent.bet)
      else:
        print('DRAW')
        agent.process_reward(0, additional_cards)
        self._print_reward(idx, False, True, 0)

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
