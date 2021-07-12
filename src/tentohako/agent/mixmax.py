import copy
import random

from .base import BaseAgent


class MinMaxAgent(BaseAgent):
    def __init__(self, name="minmax", depth=3):
        """An agents which uses minmax algorithm for search

        Args:
            name: the name of the agent
            depth: number of recursion

        Attributes:
            name: the name of the agent
            depth: number of recursion
        """
        super().__init__(name)
        self.depth = depth

    def minmax(self, board, player_id, id_to_scores, depth):
        """Search the best action with minmax algorithm

        Args:
            board: the object of Board class which represents
                   the current status
            player_id: id of this agent
            id_to_scores: dictionary whose keies are the user id and the
                          values are scores
            depth: number of recursion

        Returns:
            best: score of the given board
        """
        if depth == 0 or board.is_done():
            return id_to_scores["1"] - id_to_scores["-1"]

        next_states = []
        valid_actions = self.get_valid_action(board)
        for va in valid_actions:
            temp_state, temp_score = board.next_state(va[0], va[1])
            temp_id_to_scores = copy.deepcopy(id_to_scores)
            temp_id_to_scores[str(player_id)] += temp_score
            next_states.append((temp_state, temp_id_to_scores))

        best = -1e5 if player_id == 1 else 10 * board.nrow * board.ncol
        for i, (sta, dic) in enumerate(next_states):
            s_score = self.minmax(sta, -1 * player_id, dic, depth - 1)
            best = max(best, s_score) if player_id == 1 else min(best, s_score)

        return best

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

        next_states = []
        valid_actions = self.get_valid_action(board)
        for va in valid_actions:
            temp_state, temp_score = board.next_state(va[0], va[1])
            temp_id_to_scores = copy.deepcopy(id_to_scores)
            temp_id_to_scores[str(self.player_id)] += temp_score
            next_states.append((va, temp_state, temp_id_to_scores))

        best_score = -1e5 if self.player_id == 1 else 10 * board.nrow * board.ncol
        action_dict = {}

        for (va, sta, dic) in next_states:
            score = self.minmax(sta, -1 * self.player_id, dic, self.depth)

            if score not in action_dict:
                action_dict[score] = [va]
            else:
                action_dict[score].append(va)

            if self.player_id == 1 and score > best_score:
                best_score = score
            if self.player_id == -1 and score < best_score:
                best_score = score

        picked_action = random.choice(action_dict[best_score])

        return picked_action


class AlphaBetaAgent(MinMaxAgent):
    def __init__(self, name="alphabeta", depth=3):
        """An agents which uses alpha-beta algorithm for search

        Args:
            name: the name of the agent
            depth: number of recursion

        Attributes:
            name: the name of the agent
            depth: number of recursion
        """
        super().__init__(name=name, depth=depth)

    def alphabeta(self, board, player_id, id_to_scores, depth, alpha, beta):
        """Alpha^beta pruning

        Args:
            board: the object of Board class which represents
                   the current status
            player_id: id of this agent
            id_to_scores: dictionary whose keies are the user id and the
                          values are scores
            depth: number of recursion
            alpha: alpha value
            beta: beta value

        Returns:
            alpha, beta, or node value: if depth == 0 then return node value
                                        elif player_id == self.player_id then return alpha
                                        else player_id != self.player_id then return beta
        """
        if depth == 0 or board.is_done():
            return id_to_scores["1"] - id_to_scores["-1"]

        next_states = []
        valid_actions = self.get_valid_action(board)
        for va in valid_actions:
            temp_state, temp_score = board.next_state(va[0], va[1])
            temp_id_to_scores = copy.deepcopy(id_to_scores)
            temp_id_to_scores[str(player_id)] += temp_score
            next_states.append((temp_state, temp_id_to_scores))

        if self.player_id == player_id:
            for i, (sta, dic) in enumerate(next_states):
                alpha = max(
                    alpha,
                    self.alphabeta(sta, -1 * player_id, dic, depth - 1, alpha, beta),
                )
                # beta cut
                if alpha >= beta:
                    break
            return alpha

        else:
            for i, (sta, dic) in enumerate(next_states):
                beta = min(
                    beta,
                    self.alphabeta(sta, -1 * player_id, dic, depth - 1, alpha, beta),
                )
                # alpha cut
                if alpha >= beta:
                    break
            return beta

    def minmax(self, board, player_id, id_to_scores, depth):
        """Wrapper method for alpha-beta search

        Args:
            board: the object of Board class which represents
                   the current status
            player_id: id of this agent
            id_to_scores: dictionary whose keies are the user id and the
                          values are scores
            depth: number of recursion

        Returns:
            best: score of the given board
        """
        score = self.alphabeta(
            board, player_id, id_to_scores, depth, -float("inf"), float("inf")
        )
        return score
