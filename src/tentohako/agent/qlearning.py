import math
import pickle
import random
from collections import defaultdict

import numpy as np

from .base import BaseAgent

DEFAULT_QVALUE = 0


def _return_default_q_value():
    return DEFAULT_QVALUE


def _return_default_dict():
    return defaultdict(_return_default_q_value)


class QLearningAgent(BaseAgent):
    def __init__(self, name="q-learning", epsilon=0.2, alpha=0.4, discount=0.9):
        """An agents which uses Q-learning for search

        Args:
            name: the name of this Agent
            epsilon: how gree this agent is
            alpha: learning rete
            discount: discount rate for future rewards

        Attributes
            name: the name of this Agent
            epsilon: how gree this agent is
            alpha: learning rete
            discount: discount rate for future rewards
            _Qsa: dictionary which stores Q[(s, a)]
        """
        super().__init__(name)
        self.epsilon = epsilon
        self.alpha = alpha
        self.discount = discount

        self._Qsa = defaultdict(_return_default_dict)

    def adaptive_rate(self, t):
        """Culculate adaptive rate based on the current step

        Args:
            t: current step

        Returns:
            1.1 - max([0.1, min(1, math.log((t)/25))])
        """
        return 1.1 - max([0.1, min(1, math.log((t) / 25))])

    def state_action_to_qvalue(self, string_state, action):
        """Returns Q(state, action)

        Args:
            string_state: string representation of the state
            action: picked actino

        Returns:
            self._Qsa[string_state][action]: Q(state, action)
        """
        return self._Qsa[string_state][action]

    def set_qvalue(self, string_state, action, value):
        """Sets the Qvalue for [state, action] to the given value

        Args:
            string_state: string representation of the state
            action: picked actino
            value: QValue for (state, action)
        """
        self._Qsa[string_state][action] = value

    def board_to_max_qvalue(self, board):
        """Compute your agent's estimate of V(s) using current q-values
           V(s) = max_over_action Q(state, action) over possible actions.

        Args:
            board: the instance of Bard class

        Returns:
            value:estimated value of the state

        Note:
            please take into account that q-values can be negative.
        """
        # get possible actions
        possible_actions = self.get_valid_action(board)

        # If there are no legal actions, return 0.0
        if len(possible_actions) == 0:
            return 0.0

        # return highest Q-value
        string_state = str(board.board_matrix)
        q_values = np.array(
            [
                self.state_action_to_qvalue(string_state, action)
                for action in possible_actions
            ]
        )
        value = np.max(q_values)

        return value

    def update(self, board, action, reward, next_board, t, adaptive=False):
        """Update Q-value
           Q(s, a) := (1 - alpha) * Q(s, a) + alpha * (r + gamma * V(s'))

        Args:
            board: the current state
            action: action from the current state to the next state
            reward: reward of the current state
            next_board: next state
            t: the current step
            adaptive: use adapted learning rate or not
        """
        # adjust the learning rate
        if adaptive:
            learning_rate = self.alpha * self.adaptive_rate(t)
        else:
            learning_rate = self.alpha

        # Q(s, a) := (1 - learning_rate) * Q(s, a) + learning_rate * (r + gamma * V(s'))
        string_state = str(board.board_matrix)
        q_s_a = (1 - learning_rate) * self.state_action_to_qvalue(
            string_state, action
        ) + learning_rate * (
            reward + self.discount * self.board_to_max_qvalue(next_board)
        )

        self.set_qvalue(string_state, action, q_s_a)

    def pick_best_action(self, board):
        """Compute the best action to take in a state(using current q-values).

        Args:
            board: the current state

        Returns:
            best_action: the best action
        """
        # get possible actions
        possible_actions = self.get_valid_action(board)

        # If there are no legal actions, return None
        if len(possible_actions) == 0:
            return None

        # return the action with highest Q-value
        string_state = str(board.board_matrix)
        q_values = np.array(
            [
                self.state_action_to_qvalue(string_state, action)
                for action in possible_actions
            ]
        )
        best_index = np.argmax(q_values)
        best_action = possible_actions[best_index]

        return best_action

    def pick_action(self, board):
        """Compute the action to take in the current state, including exploration.
           With probability self.epsilon, we should take a random action.
           otherwise - the best policy action (self.getPolicy).

        Args:
            board: the current state

        Returns:
            picked_action: chosen action
        """
        # get possible actions
        possible_actions = self.get_valid_action(board)

        # If there are no legal actions, return None
        if len(possible_actions) == 0:
            return None

        # e-greedy
        best_or_random = np.random.binomial(n=1, p=self.epsilon)
        if best_or_random == 0:
            picked_action = self.pick_best_action(board)
        else:
            picked_action = random.choice(possible_actions)

        return picked_action

    def eval(self):
        """Set the epsilon to zero"""
        self.epsilon = 0

    def step(self, board, id_to_scores):
        """Return the action based on the given board.

        Args:
            board: the instance of Board class which represents
                   the current board state.
            id_to_scores: dictionary whose keies are the user id and the
                          values are scores

        Returns:
            picked_action:
        """

        picked_action = self.pick_action(board)
        return picked_action

    def save(self, path):
        """Save self._qvalue which represets the Q[(s a)]

        Args:
            path: output path
        """
        with open(path, mode="wb") as f:
            pickle.dump(self._Qsa, f)

    def load(self, path):
        """Load pickle which represets the Q[(s a)]

        Args:
            path: path to pickle
        """
        with open(path, mode="rb") as f:
            self._Qsa = pickle.load(f)
