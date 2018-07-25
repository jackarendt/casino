from actor import *
from player import *

class HumanActor(Actor):

  def process_state(self, state):
    return STAND
