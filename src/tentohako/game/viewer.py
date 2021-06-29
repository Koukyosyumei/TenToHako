import os

import matplotlib.animation as animation
from matplotlib import pyplot as plt
from PIL import Image


class Viewer:
    def __init__(self, board, height=6, width=6, tmp_dir="tmp",
                 id_to_color={1: "b", -1: "r"}, text_fontsize=36):
        self.fig = plt.figure(figsize=(height, width))
        self.board = board
        self.tmp_dir = tmp_dir
        self.text_fontsize = text_fontsize

        self.dots = sum([[(x, y) for y in range(board.nrow+1)]
                         for x in range(board.ncol+1)], [])
        self.xs = [d[0]*2 for d in self.dots]
        self.ys = [d[1]*2 for d in self.dots]

        self.id_to_color = id_to_color
        self.im_log = []
        os.makedirs(tmp_dir, exist_ok=True)

    def update_board(self, new_board):
        self.board = new_board

    def update(self, step, player_id, action_i, action_j):
        if step == 0:
            points = {}
            for i in range(self.board.dim_y):
                for j in range(self.board.dim_x):
                    if i % 2 == 1 and j % 2 == 1:
                        points[(j, i)] = self.board.board_matrix[i][j]

            plt.scatter(self.xs, self.ys, c="k")

            for k, v in points.items():
                plt.text(k[0], k[1], v,
                         fontsize=self.text_fontsize, ha='center', va='center')

        else:
            if action_j % 2 == 0 and action_i % 2 == 1:
                self.board.board_matrix[action_j][action_i] = "-"

                plt.hlines(y=action_j, xmin=action_i-1,
                           xmax=action_i+1, linewidths=5,
                           color=self.id_to_color[player_id])

                if action_j < self.board.dim_y - 1:
                    # j+1 i
                    if self.board.board_matrix[action_j+2][action_i] == '-' and\
                            self.board.board_matrix[action_j+1][action_i+1] == '|' and\
                            self.board.board_matrix[action_j+1][action_i-1] == '|':
                        plt.fill([action_i-1, action_i+1, action_i+1, action_i-1],
                                 [action_j, action_j, action_j+2, action_j+2], alpha=0.3,
                                 color=self.id_to_color[player_id])

                if action_j > 0:
                    # j-1, i
                    if self.board.board_matrix[action_j-2][action_i] == '-' and\
                            self.board.board_matrix[action_j-1][action_i+1] == '|' and\
                            self.board.board_matrix[action_j-1][action_i-1] == '|':
                        plt.fill([action_i-1, action_i+1, action_i+1, action_i-1],
                                 [action_j-2, action_j-2, action_j, action_j], alpha=0.3,
                                 color=self.id_to_color[player_id])

            else:
                self.board.board_matrix[action_j][action_i] = '|'

                plt.vlines(x=action_i, ymin=action_j-1,
                           ymax=action_j+1, linewidths=5,
                           color=self.id_to_color[player_id])

                if action_i < self.board.dim_x - 1:
                    # j, i+1
                    if self.board.board_matrix[action_j][action_i+2] == '|' and\
                        self.board.board_matrix[action_j+1][action_i+1] == '-' and\
                            self.board.board_matrix[action_j-1][action_i+1] == '-':
                        plt.fill([action_i, action_i+2, action_i+2, action_i],
                                 [action_j-1, action_j-1, action_j+1, action_j+1], alpha=0.3,
                                 color=self.id_to_color[player_id])
                if action_i > 0:
                    # j, i-1
                    if self.board.board_matrix[action_j][action_i-2] == '|' and\
                        self.board.board_matrix[action_j+1][action_i-1] == '-' and\
                            self.board.board_matrix[action_j-1][action_i-1] == '-':
                        plt.fill([action_i-2, action_i, action_i, action_i-2],
                                 [action_j-1, action_j-1, action_j+1, action_j+1], alpha=0.3,
                                 color=self.id_to_color[player_id])

        plt.axis([-0.1, self.board.dim_x-1+0.1,
                  self.board.dim_y-1+0.1, -0.1])
        plt.xticks(color="None")
        plt.yticks(color="None")
        plt.tick_params(length=0)
        plt.title(f"step {step}, player {player_id}")

        plt.savefig(self.tmp_dir + f"/{step}.png")
        self.im_log.append(self.tmp_dir + f"/{step}.png")

    def save(self, path, interval=300, repear_delay=1000):
        fig = plt.figure()
        ims = []
        for impath in self.im_log:
            tmp = Image.open(impath)
            ims.append([plt.imshow(tmp)])
            os.remove(impath)

        plt.xticks(color="None")
        plt.yticks(color="None")
        plt.tick_params(length=0)

        anim = animation.ArtistAnimation(
            fig, ims, interval=interval, repeat_delay=repear_delay)
        anim.save(path, writer="imagemagick")

        try:
            os.rmdir(self.tmp_dir)
        except OSError as e:
            pass
