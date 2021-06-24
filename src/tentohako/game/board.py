import copy
import random


class Board:
    def __init__(self, board_matrix, ncol, nrow,
                 score_min=1, score_max=9):
        self.board_matrix = board_matrix
        self.ncol = ncol
        self.nrow = nrow
        self.score_min = score_min
        self.score_max = score_max
        self.dim_x = ncol*2 + 1
        self.dim_y = nrow*2 + 1

    def initialize(self):
        for i in range(self.dim_y):
            r = []
            for j in range(self.dim_x):
                if i % 2 == 1 and j % 2 == 1:
                    r.append(random.randint(self.score_min, self.score_max))
                elif i % 2 == 0 and j % 2 == 0:
                    r.append("*")
                else:
                    r.append(" ")
            self.board_matrix.append(r)

    def next_state(self, j, i):
        score = 0
        next_board = copy.deepcopy(self)

        if i % 2 == j % 2:
            raise ValueError("i % 2 should not be equal to j % 2")

        elif j % 2 == 0 and i % 2 == 1:
            next_board.board_matrix[j][i] = "-"
            if j < next_board.dim_y - 1:
                if next_board.board_matrix[j+2][i] == '-' and\
                        next_board.board_matrix[j+1][i+1] == '|' and\
                        next_board.board_matrix[j+1][i-1] == '|':
                    score += next_board.board_matrix[j+1][i]
            if j > 0:
                if next_board.board_matrix[j-2][i] == '-' and\
                        next_board.board_matrix[j-1][i+1] == '|' and\
                        next_board.board_matrix[j-1][i-1] == '|':
                    score += next_board.board_matrix[j-1][i]

        else:
            next_board.board_matrix[j][i] = '|'
            if i < next_board.dim_x - 1:
                if next_board.board_matrix[j][i+2] == '|' and\
                    next_board.board_matrix[j+1][i+1] == '-' and\
                        next_board.board_matrix[j-1][i+1] == '-':
                    score += next_board.board_matrix[j][i+1]
            if i > 0:
                if next_board.board_matrix[j][i-2] == '|' and\
                    next_board.board_matrix[j+1][i-1] == '-' and\
                        next_board.board_matrix[j-1][i-1] == '-':
                    score += next_board.board_matrix[j][i-1]

        return next_board, score

    def is_done(self):
        for j in range(self.dim_y):
            for i in range(self.dim_x):
                if (i % 2 != j % 2) and (self.board_matrix[j][i] == " "):
                    return False
        return True

    def board_to_string(self):
        boardstring = ""
        if self.dim_x > 9:
            boardstring += " "
        boardstring += "   "

        for i in range(self.dim_x):
            if (i % 2 == 0):
                boardstring += str(int(i / 2))
                boardstring += ' '*(5 - int(i/2)//10)
        boardstring += "\n"

        if self.dim_x > 9:
            boardstring += " "
        boardstring += "   "

        for i in range(self.dim_x + 1):
            boardstring += "___"
        boardstring += "\n"

        for j in range(self.dim_y):
            if self.dim_x > 9 and (j/2) < 10:
                boardstring += " "
            if (j % 2 == 0):
                boardstring += str(int(j/2)) + "| "
            else:
                boardstring += " "*len(str(int((j-1)/2))) + "| "
            for z in range(self.dim_x):
                boardstring += str(self.board_matrix[j][z])
                boardstring += '  '
            boardstring += "\n"

        return boardstring
