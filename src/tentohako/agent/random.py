import random

from .base import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self, name="random"):
        super().__init__(name)

    def step(self, board):
        valid_actions = self.get_valid_action(board)
        return random.choice(valid_actions)
