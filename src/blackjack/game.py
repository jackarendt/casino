from blackjack.constants import *
from blackjack.dealer_actor import DealerActor
from blackjack.human_actor import HumanActor
from blackjack.shoe import Shoe

class Blackjack(object):
  """
  An environment focused on playing blackjack. Can be played by a human or
  agent. Agents should override `Actor` to provide custom functionality based on
  the current state. An advantage of using this environment is that it allows
  for many actors to play at once and accumulate different experiences.
  """
  def __init__(self, num_agents, print_desc, is_human):
    # A typical shoe has 6 decks and reshuffles when roughly 5/6 decks are used.
    self.shoe = Shoe(6, 0.8)
    self.dealer = DealerActor(1000000)
    self.agents = []
    self.player_count = num_agents + 1
    self.print_desc = print_desc

    # Add the agents.
    for i in range(num_agents):
      if is_human:
        agent = HumanActor(1000)
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
        self.dealer.add_card(card)
      else:
        self.agents[i % self.player_count].add_card(card)

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
      self.play_agent(agent, idx)

    self.dealer.show_hand = True
    if self.print_desc:
      print('Dealer: ' + str(self.dealer))

    # Assess the dealer actions.
    self.play_dealer(self.dealer)

    if self.print_desc:
      print('[FINAL] Dealer: ' + str(self.dealer))
      print('-------------------------')

  def assess_rewards(self):
    """Finalizes the hand and either takes or hands out winnings."""
    dealer_count = self.dealer.count()
    self.dealer.process_reward(0, 0)

    for idx, agent in enumerate(self.agents):
      # Other rewards are the number of cards that were drawn.
      additional_cards = agent.drawn_cards()
      running_reward = 0

      # Iterate through all of the hands of the agent and assess how they
      # performed.
      for hand_idx, hand in enumerate(agent.hands):
        # Get the new reward from the hand and update the running reward.
        new_reward = self.compare_hands(dealer_count, agent.count(hand_idx),
            agent.is_blackjack(hand_idx), agent.bet)
        running_reward += new_reward

        if self.print_desc:
          won = new_reward > 0
          draw = new_reward == 0
          self._print_reward(idx, hand_idx, won, draw, new_reward)

      if self.print_desc:
        print('\n\n')

      # Process the rewards at the end of each agent's calculation.
      agent.process_reward(running_reward, agent.drawn_cards())

  def compare_hands(self, dealer, player, blackjack, bet):
    dealer_bust = dealer > BLACKJACK_VALUE
    player_bust = player > BLACKJACK_VALUE

    loss = player_bust or (player < dealer and not dealer_bust)
    win = (dealer_bust or player > dealer or blackjack) and not player_bust

    if win:
      return (1.5 if blackjack else 1) * bet
    elif loss:
      return -1 * bet
    else:
      return 0

  def play_agent(self, agent, idx):
    hand_idx = 0
    while hand_idx < len(agent.hands):
      self.play_hand(agent, idx, hand_idx)
      hand_idx += 1
    if self.print_desc:
      if len(agent.hands) == 1:
        print('[FINAL] Player ' + str(idx + 1) + ': ' + str(agent))
      else:
        print('[FINAL] Player ' + str(idx + 1) + ':\n' + str(agent))


  def play_hand(self, agent, idx, hand_idx):
    """
    Plays an individual hand for an agent.
    agent Agent:
      - The agent that is currently playing.
    idx Int:
      - The index of the agent that is playing.
    hand_idx Int:
      - The index of the hand that is currently being played.
    """
    # Splitting aces only allows for one card to be drawn for each hand.
    # Therefore, don't allow any actions on the second split hand.
    hand = agent.hands[hand_idx]
    print(hand)
    if hand.is_split:
      if self.print_desc:
        print('Player ' + str(idx + 1) + ' (' + str(hand_idx) + '): ' +
              str(agent.hands[hand_idx]))
      if hand.cards[0].is_ace():
        return

    d = False
    while not d:
      # The count should be adjusted such that the dealer's second card count
      # isn't revealed.
      count = self.shoe.hilo_count() - self.dealer.hidden_card().hilo_count()
      state = {
        DEALER_STATE_KEY: self.dealer.first_card(),
        COUNT_STATE_KEY: count,
        DOUBLE_DOWN_STATE_KEY: hand.can_double_down(),
        SPLIT_STATE_KEY: hand.can_split()
      }

      # Process the current state.
      a = agent.process_state(state)

      # Add the card if the user hit.
      if a == Action.HIT or a == Action.DOUBLE_DOWN:
        agent.add_card(self.shoe.draw(), hand_idx)

      split_finished = False
      if a == Action.SPLIT:
        # Split the hands into two hands.
        split_finished = hand.cards[0].is_ace()
        agent.split_hand(hand_idx)
        agent.add_card(self.shoe.draw(), hand_idx)
        agent.add_card(self.shoe.draw(), hand_idx + 1)

      # Print the description after the user takes their action.
      if self.print_desc and a != Action.STAND:
        print('Player ' + str(idx + 1) + ' (' + str(hand_idx) + '): ' +
              str(agent.hands[hand_idx]))

      # The agent is finished after they stand, or double down. A controversial,
      # but relatively accepted rule is only receiving one card for splitting
      # aces.
      d = (a == Action.STAND or a == Action.DOUBLE_DOWN or
           hand.count() > BLACKJACK_VALUE or split_finished)

  def play_dealer(self, dealer):
    """Plays the dealer's hand."""
    d = False
    while not d:
      a = dealer.process_state({})
      if a == Action.HIT:
        dealer.add_card(self.shoe.draw())
        if self.print_desc:
          print('Dealer: ' + str(dealer))

      # Dealer is done when they stand or bust.
      d = a == Action.STAND or dealer.count() >= BLACKJACK_VALUE

  def _print_reward(self, agent_idx, hand_idx, won, draw, reward):
    if not self.print_desc:
      return

    player_desc = 'Player ' + str(agent_idx + 1) + ' (' + str(hand_idx) + ')'
    if won:
      print(player_desc + ' won. +' + str(reward))
    elif draw:
      print(player_desc + ' pushed.')
    else:
      print(player_desc + ' lost. ' + str(reward))
