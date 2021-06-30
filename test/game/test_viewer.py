import shutil


def test_viewer():
    from tentohako.game import Board, Viewer
    board = Board([], 2, 2)
    board.initialize()

    board_matrix = [['*', '-', '*', '-', '*'],
                    ['|',  8,  '|',  2,  '|'],
                    ['*', ' ', '*', ' ', '*'],
                    [' ',  5,  '|',  3,  '|'],
                    ['*', '-', '*', '-', '*']]
    next_board_matrix = [['*', '-', '*', '-', '*'],
                         ['|', 8, '|', 2, '|'],
                         ['*', '-', '*', ' ', '*'],
                         [' ', 5, '|', 3, '|'],
                         ['*', '-', '*', '-', '*']]

    board.board_matrix = board_matrix
    tmp_dir = "tmp"
    viewer = Viewer(board, tmp_dir=tmp_dir)
    viewer.update_board(board)
    viewer.update(1, 1, 1, 2)
    assert viewer.board.board_matrix == next_board_matrix

    shutil.rmtree(tmp_dir)
