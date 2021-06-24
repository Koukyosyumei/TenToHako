from .board import Board


class BaseGame:
    def __init__(self, player_ids, ncol, nrow,
                 score_min=1, score_max=9):
        self.player_ids = player_ids
        self.board = Board([], ncol, nrow, score_min, score_max)

        self.board.initialize()
        self.num_of_players = len(self.player_ids)
        self.scores = {idx: 0 for idx in self.player_ids}
        self.current_step = 0

    def play(self, steps_limit=1e10):
        pass
