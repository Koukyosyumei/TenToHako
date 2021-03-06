import random

from .base import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self, name="random"):
        """An agents which randomly returns an action

        Args:
            name: the name of the agent

        Attributes:
            name: the name of the agent
        """
        super().__init__(name)

    def step(self, board, id_to_scores):
        """Randomly return the action based on the given board.

        Args:
            board: the instance of Board class which represents
                   the current board state.
            id_to_scores: dictionary whose keies are the user id and the
                          values are scores

        Returns:
            picked_action: randomly chosen action
        """
        valid_actions = self.get_valid_action(board)
        picked_action = random.choice(valid_actions)
        return picked_action
