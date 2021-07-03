import argparse
import random

import numpy as np
from matplotlib import pyplot as plt
from tentohako.agent import MinMaxAgent, QLearningAgent, RandomAgent, UCTAgent
from tentohako.game import Board
from tqdm import tqdm


def main(iterations, ncol, nrow, score_min, score_max,
         model_path, qlearnagent, opponent, log_path):

    history = []

    for i in tqdm(range(iterations)):
        board = Board([], ncol, nrow, score_min=score_min,
                      score_max=score_max)
        board.initialize()
        id_to_scores = {"1": 0, "-1": 0}

        if random.randint(0, 9) % 2 == 0:
            opponent.set_player_id(1)
            qlearnagent.set_player_id(-1)
            id_to_agent = {1: opponent, -1: qlearnagent}
            player_to_learn = [-1]
        else:
            opponent.set_player_id(-1)
            qlearnagent.set_player_id(1)
            id_to_agent = {-1: opponent, 1: qlearnagent}
            player_to_learn = [1]

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
                history.append(reward)

            """
            # intermidiate reward
            else:
                reward = (id_to_scores[str(qlearnagent.player_id)] -
                          id_to_scores[str(-qlearnagent.player_id)])/8
            """

            if active_player in player_to_learn:
                id_to_agent[active_player].update(board, picked_act,
                                                  reward,
                                                  next_board, t,
                                                  adaptive=False)

            active_player *= -1
            board = next_board
            t += 1

    qlearnagent.save(model_path)
    plt.plot((np.array(history).reshape(100, -1) == 1).mean(axis=0),
             alpha=0.4)
    plt.plot((np.array(history).reshape(100, -1) == -1).mean(axis=0),
             alpha=0.4)
    plt.savefig(log_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="number of iterations",
                        type=int, default=100)
    parser.add_argument("-r", help="number of rows",
                        type=int, default=3)
    parser.add_argument("-c", help="number of columns",
                        type=int, default=3)
    parser.add_argument("-e", help="epsilon",
                        type=float, default=0.2)
    parser.add_argument("-a", help="alpha",
                        type=float, default=0.4)
    parser.add_argument("-d", help="discount rate",
                        type=float, default=0.9)
    parser.add_argument("--smi", help="min of score",
                        type=int, default=1)
    parser.add_argument("--sma", help="max of score",
                        type=int, default=9)
    parser.add_argument("-o",
                        help="opponent agent type r: random, m: minmax,\
                        u: uct",
                        type=str, default="r")
    parser.add_argument("--mp", help="path to the output pickle",
                        type=str, default="model.pickle")
    parser.add_argument("--lp", help="path to the output picture",
                        type=str, default="win-rate.png")
    args = parser.parse_args()

    qlearnagent = QLearningAgent("q-learning",
                                 epsilon=args.e,
                                 alpha=args.a,
                                 discount=args.d)
    if args.o == "r":
        opponent = RandomAgent()
    elif args.o == "m":
        opponent = MinMaxAgent()
    elif args.o == "u":
        opponent = UCTAgent()

    main(args.n, args.c, args.r, args.smi, args.sma,
         args.mp, qlearnagent, opponent, args.lp)
