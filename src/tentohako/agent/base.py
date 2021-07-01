class BaseAgent:
    def __init__(self, name=""):
        """Abstract class which represents the agent.

        Args:
            name: the name of the agent

        Attributes:
            name: the name of the agent
        """
        self.name = name

    def set_player_id(self, player_id):
        self.player_id = player_id

    def step(self, board, id_to_scores):
        """Return the action based on the given board.

        Args:
            board: the instance of Board class which represents
                   the current board state.
            id_to_scores: dictionary whose keys are user id and values
                          are scores.
        """
        pass

    def get_valid_action(self, board):
        """Return a list of possible actions based on the given board.

        Args:
            board: the instance of Board class which represents
                   the current board state.

        Returns:
            valid_actions: a list of possible actions
        """
        valid_actions = []
        for j in range(board.dim_y):
            for i in range(board.dim_x):
                if (i % 2 != j % 2) and (board.board_matrix[j][i] == " "):
                    valid_actions.append((j, i))
        return valid_actions
