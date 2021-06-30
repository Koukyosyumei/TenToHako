

def test_board():
    from tentohako.game import Board

    board_matrix = [['*', '-', '*', '-', '*'],
                    ['|',  8,  '|',  2,  '|'],
                    ['*', ' ', '*', ' ', '*'],
                    [' ',  5,  '|',  3,  '|'],
                    ['*', '-', '*', '-', '*']]

    board = Board([], 2, 2)
    board.initialize()

    assert board.dim_x == 5
    assert board.dim_y == 5

    for j in range(board.dim_y):
        for i in range(board.dim_x):
            if i % 2 == 1 and j % 2 == 1:
                assert board.board_matrix[j][i] in\
                    list(range(board.score_min, board.score_max+1))
            elif i % 2 == 0 and j % 2 == 0:
                assert board.board_matrix[j][i] == "*"
            else:
                assert board.board_matrix[j][i] == " "

    board.board_matrix = board_matrix
    assert board.is_done() is False

    next_board_matrix = [['*', '-', '*', '-', '*'],
                         ['|', 8, '|', 2, '|'],
                         ['*', '-', '*', ' ', '*'],
                         [' ', 5, '|', 3, '|'],
                         ['*', '-', '*', '-', '*']]
    next_board, score = board.next_state(2, 1)
    assert next_board.board_matrix == next_board_matrix
    assert score == 8

    next_board, score = next_board.next_state(2, 3)
    next_board, score = next_board.next_state(3, 0)
    assert next_board.is_done() is True
