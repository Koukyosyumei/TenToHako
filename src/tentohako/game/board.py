import copy
import random


class Board:
    def __init__(self, board_matrix, ncol, nrow,
                 score_min=1, score_max=9):
        """Class represents the board of the dots and boxes

        Args:
            board_matrix: list which represents the current state of the board
            ncol: number of the columns of the board
            nrow: number of the row of the board
            score_min: the minimum score of the cell
            score_max: the mamimum score of the cell

        Arguments:
            board_matrix: list which represents the current state of the board
            ncol: number of the columns of the board
            nrow: number of the row of the board
            score_min: the minimum score of the cell
            score_max: the mamimum score of the cell
            dim_x: the x element of the dimension of the board_matrix
                   (equal to ncol*2 + 1)
            dim_y: the y element of the dimension of the board_matrix
                   (equal to nrow*2 + 1)
        """
        self.board_matrix = board_matrix
        self.ncol = ncol
        self.nrow = nrow
        self.score_min = score_min
        self.score_max = score_max
        self.dim_x = ncol*2 + 1
        self.dim_y = nrow*2 + 1

    def initialize(self):
        """Initialize the board matrix.
           Each cell is filled randomly with a number between
           score_min and score_max.
        """
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
        """Make next state and culculate the score based on the given action.

        Args:
            j: y element of the picked action.
            i: x element of the picked action.

        Returns:
            next_board: the instance of Board class which represents the next state.
            score: score the agent got with the picked action.
        """
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
        """Judge whether the state meets the enc condition.

        Returns:
            bool: True if the game is over.
        """
        for j in range(self.dim_y):
            for i in range(self.dim_x):
                if (i % 2 != j % 2) and (self.board_matrix[j][i] == " "):
                    return False
        return True

    def board_to_string(self):
        """Convert the board matrix to string to print our.

        Returns:
            boardstring: the string representataion of the board matrix.
        """
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
