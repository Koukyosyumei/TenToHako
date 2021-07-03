import os
import random


def test_qlearningagent():

    from tentohako.agent import QLearningAgent
    from tentohako.game import Board

    board_matrix = [['*', '-', '*', '-', '*'],
                    ['|',  8,  '|',  2,  '|'],
                    ['*', ' ', '*', ' ', '*'],
                    [' ',  5,  '|',  3,  '|'],
                    ['*', '-', '*', '-', '*']]
    name = "q-learning"
    player_id = 1
    id_to_scores = {'1': 0, '-1': 0}

    board = Board([], 2, 2)
    board.initialize()
    board.board_matrix = board_matrix

    qlearningagent = QLearningAgent(name)
    qlearningagent.set_player_id(player_id)
    qlearningagent.load(
        "saved_models/qlearning_ncol_2_nrow_2_scoremin_1_scoremax_9_iterations_10000.pickle")
    valid_actions = qlearningagent.get_valid_action(board)
    picked_action = qlearningagent.step(board, id_to_scores)

    assert qlearningagent.name == name
    assert qlearningagent.player_id == player_id
    assert valid_actions == [(2, 1), (2, 3), (3, 0)]
    assert picked_action in valid_actions


def test_qlearningagent_learn():

    from tentohako.agent import QLearningAgent, RandomAgent
    from tentohako.game import Board

    ncol = 2
    nrow = 2
    score_min = 1
    score_max = 3

    randomagent = RandomAgent("random")
    qlearnagent = QLearningAgent("q-learning")

    iterations = 5
    turns = 0

    for i in range(iterations):
        board = Board([], ncol, nrow, score_min=score_min,
                      score_max=score_max)
        board.initialize()
        id_to_scores = {"1": 0, "-1": 0}

        if random.randint(0, 9) % 2 == 0:
            randomagent.set_player_id(1)
            qlearnagent.set_player_id(-1)
            id_to_agent = {1: randomagent, -1: qlearnagent}
            player_to_learn = [-1]
        else:
            randomagent.set_player_id(-1)
            qlearnagent.set_player_id(1)
            id_to_agent = {-1: randomagent, 1: qlearnagent}
            player_to_learn = [1]
            turns += 1

        active_player = 1
        t = 0
        while not board.is_done():
            picked_act = id_to_agent[active_player].step(board, id_to_scores)
            next_board, score = board.next_state(picked_act[0], picked_act[1])
            id_to_scores[str(active_player)] += score

            reward = 0
            if next_board.is_done():
                if id_to_scores[str(qlearnagent.player_id)] >\
                        id_to_scores[str(-qlearnagent.player_id)]:
                    reward = 1
                elif id_to_scores[str(qlearnagent.player_id)] ==\
                        id_to_scores[str(-qlearnagent.player_id)]:
                    reward = 0
                else:
                    reward = -1
            else:
                reward = (id_to_scores[str(qlearnagent.player_id)] -
                          id_to_scores[str(-qlearnagent.player_id)])/8

            if active_player in player_to_learn:
                id_to_agent[active_player].update(board, picked_act, reward,
                                                  next_board, t,
                                                  adaptive=False)

            active_player *= -1
            board = next_board
            t += 1

    qlearnagent.save("test.pickle")
    qlearnagent.load("test.pickle")
    os.remove("test.pickle")
