

def get_valid_action(board):
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


class Node:
    def __init__(self, parentNode, board, action, activePlayer, id_to_scores):
        self.action = action
        self.parentNode = parentNode
        self.children = []
        self.wins = 0
        self.visits = 0
        self.unexamined = get_valid_action(board)
        self.activePlayer = activePlayer
        self.id_to_scores = id_to_scores

    def addChild(self, board, index, id_to_scores):
        node = Node(
            self, board, self.unexamined[index],
            self.action_player*-1, id_to_scores)
        del self.unexamined[index]
        self.children.append(node)
        return node

    def selectChild(self):
        pass

    def update(self, result, player_id):
        self.visits += 1
        self.wins += result[player_id]

    def mostVisitedChild(self):
        mostVisited = self.children[0]
        for i, child in enumerate(self.children):
            if (child.visits > mostVisited.visits):
                mostVisited = child

        return mostVisited
