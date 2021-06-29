from tentohako.agent import RandomAgent
from tentohako.game import Board

if __name__ == '__main__':
    board = Board([], 2, 2)
    board.initialize()
    print(board.board_to_string())
    print("------")
    randomagent = RandomAgent(0)
    action = randomagent.step(board)
    print(action)
    next_board, score = board.next_state(action[0], action[1])
    print(next_board.board_to_string())
    print(board.board_to_string())
    """
    board.action(1, 0)
    print(board.board_to_string())
    print("------")
    board.action(1, 2)
    print(board.board_to_string())
    """
