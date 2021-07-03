def test_minmaxagent():
    from tentohako.agent import MinMaxAgent
    from tentohako.game import Board

    board_matrix = [
        ["*", "-", "*", "-", "*"],
        ["|", 8, "|", 2, "|"],
        ["*", " ", "*", " ", "*"],
        [" ", 5, "|", 3, "|"],
        ["*", "-", "*", "-", "*"],
    ]
    name = "minmax"
    depth = 2
    player_id = 1
    id_to_scores = {"1": 0, "-1": 0}

    board = Board([], 2, 2)
    board.initialize()
    board.board_matrix = board_matrix

    minmaxagent = MinMaxAgent(name, depth=depth)
    minmaxagent.set_player_id(player_id)
    valid_actions = minmaxagent.get_valid_action(board)
    picked_action = minmaxagent.step(board, id_to_scores)
    minmaxscore_depth_1 = minmaxagent.minmax(board, player_id, id_to_scores, 1)
    minmaxscore_depth_2 = minmaxagent.minmax(board, player_id, id_to_scores, 2)

    assert minmaxagent.name == name
    assert minmaxagent.player_id == player_id
    assert valid_actions == [(2, 1), (2, 3), (3, 0)]
    assert picked_action == (2, 1)
    assert minmaxscore_depth_1 == 8
    assert minmaxscore_depth_2 == 3
