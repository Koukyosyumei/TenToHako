import copy
import random

from .base import BaseAgent


class QLearningAgent(BaseAgent):
    def __init__(self, name="q-learning", e=0.2, alpha=0.003, gamma=0.9):
        super().__init__(name)
        self.e = e
        self.alpha = alpha
        self.gamma = gamma

        self.q = {}
        self.last_move = None
        self.last_state = None
        self.totalgamecount = 0
        self.initial_q = 1

    def policy(self, board):
        board_matrix_string = str(board.board_matrix)
        self.last_state = copy.deepcopy(board_matrix_string)
        valid_actions = self.get_valid_action(board)

        if random.random() < (self.e / (self.totalgamecount // 10000 + 1)):
            picked_action = random.choice(valid_actions)
        else:
            qs = [self.get_Q(board_matrix_string, act)
                  for act in valid_actions]
            q_max = max(qs)
            best_actions = [valid_actions[i]
                            for i, q in enumerate(qs) if q == q_max]
            picked_action = random.choice(best_actions)
            self.last_move = picked_action

        return picked_action

    def step(self, board, id_to_scores):
        picked_action = self.policy(board)
        return picked_action

    def get_Q(self, board_matrix_string, act):
        if self.q.get((board_matrix_string, act, self.player_id)) is None:
            self.q[(board_matrix_string, act, self.player_id)] = self.initial_q

        return self.q.get((board_matrix_string, act, self.player_id))

    def learn(self, board, id_to_scores):
        if self.last_move is not None:
            if not board.is_done():
                self.update_Q(self.last_state, self.last_move, 0, board)

            else:
                if id_to_scores[str(self.player_id)] >\
                        id_to_scores[str(-1*self.player_id)]:
                    self.update_Q(self.last_state, self.last_move, 1, board)
                elif id_to_scores[str(self.player_id)] <\
                        id_to_scores[str(-self.player_id)]:
                    self.update_Q(self.last_state, self.last_move, -1, board)
                else:
                    self.update_Q(self.last_state, self.last_move, 0, board)

                self.totalgamecount += 1
                self.last_move = None
                self.last_state = None

    def update_Q(self, s, a, r, fs):
        q_value = self.get_Q(s, a)
        if fs.is_done:
            new_max_Q = 0
        else:
            new_max_Q = max([self.getQ(str(fs.board_matrix), act)
                             for act in fs.get_valid_actions()])

        self.q[(s, a, self.player_id)] = q_value + self.alpha * \
            ((r+self.gamma*new_max_Q) - q_value)
