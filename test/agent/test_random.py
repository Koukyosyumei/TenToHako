def test_randomagent():

    from tentohako.agent import RandomAgent
    from tentohako.game import Board

    board_matrix = [
        ["*", "-", "*", "-", "*"],
        ["|", 8, "|", 2, "|"],
        ["*", " ", "*", " ", "*"],
        [" ", 5, "|", 3, "|"],
        ["*", "-", "*", "-", "*"],
    ]
    name = "random"
    player_id = 1
    id_to_scores = {"1": 0, "-1": 0}

    board = Board([], 2, 2)
    board.initialize()
    board.board_matrix = board_matrix

    randomagent = RandomAgent(name)
    randomagent.set_player_id(player_id)
    valid_actions = randomagent.get_valid_action(board)
    picked_action = randomagent.step(board, id_to_scores)

    assert randomagent.name == name
    assert randomagent.player_id == player_id
    assert valid_actions == [(2, 1), (2, 3), (3, 0)]
    assert picked_action in valid_actions
