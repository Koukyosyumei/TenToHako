def test_uctagent():

    from tentohako.agent import UCTAgent
    from tentohako.game import Board

    board_matrix = [
        ["*", "-", "*", "-", "*"],
        ["|", 8, "|", 2, "|"],
        ["*", " ", "*", " ", "*"],
        [" ", 5, "|", 3, "|"],
        ["*", "-", "*", "-", "*"],
    ]
    name = "uct"
    player_id = 1
    id_to_scores = {"1": 0, "-1": 0}

    board = Board([], 2, 2)
    board.initialize()
    board.board_matrix = board_matrix

    uctagent = UCTAgent(name)
    uctagent.set_player_id(player_id)
    valid_actions = uctagent.get_valid_action(board)
    picked_action = uctagent.step(board, id_to_scores)

    assert uctagent.name == name
    assert uctagent.player_id == player_id
    assert valid_actions == [(2, 1), (2, 3), (3, 0)]
    assert picked_action in valid_actions
