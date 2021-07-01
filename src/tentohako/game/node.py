

def get_valid_action_with_basic_rule(board):
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
        """Basic class which represents a node which stores the trajectory of the game.
           This class is mainly used for tree search algorithm.

        Args:
            parentNode: a node which represents the previous state
            board: current board
            action: an action which made the current board from the
                    previous state
            activePlayer: a current active player
            id_to_scores: current score status

        Attributes:
            parentNode: a node which represents the previous state
            board: current board
            action: an action which made the current board from the
                    previous state
            activePlayer: a current active player
            id_to_scores: current score status
            children: list of the child nodes
            wins: number of wins from this node
            visits: number of trials from this node
            unexamined: valid action from the current node
        """
        self.action = action
        self.parentNode = parentNode
        self.board = board
        self.children = []
        self.wins = 0
        self.visits = 0
        self.unexamined = get_valid_action_with_basic_rule(board)
        self.activePlayer = activePlayer
        self.id_to_scores = id_to_scores

    def addChild(self, board, index, id_to_scores):
        """Add a child node to this node.

        Args:
            board: the instance of the Board class which represents the next
                   status from the current node
            index: index of the valid action
            id_to_scores: score status of the child node

        Returns:
            node: the child node
        """
        node = Node(
            self, board, self.unexamined[index],
            self.action_player*-1, id_to_scores)
        del self.unexamined[index]
        self.children.append(node)
        return node

    def selectChild(self):
        """Select the child node for searching
        """
        pass

    def update(self, result, player_id):
        """Update the visit history of this node.

        Args:
            result: result of the game from this node.
            player_id: id of the player (basically equal to the activePlayer)
        """
        self.visits += 1
        self.wins += result[player_id]

    def mostVisitedChild(self):
        """Return most visited child node.

        Returns:
            mostVisited: most visited child node.
        """
        mostVisited = self.children[0]
        for i, child in enumerate(self.children):
            if (child.visits > mostVisited.visits):
                mostVisited = child

        return mostVisited
