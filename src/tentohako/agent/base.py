class BaseAgent:
    def __init__(self, player_id):
        self.player_id = player_id

    def step(self, board):
        pass

    def get_valid_action(self, board):
        valid_actions = []
        for j in range(board.dim_y):
            for i in range(board.dim_x):
                if (i % 2 != j % 2) and (board.board_matrix[j][i] == " "):
                    valid_actions.append((j, i))
        return valid_actions
