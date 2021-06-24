import random

from .base import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self, player_id):
        super().__init__(player_id)

    def step(self, board):
        valid_actions = self.get_valid_action(board)
        return random.choice(valid_actions)
