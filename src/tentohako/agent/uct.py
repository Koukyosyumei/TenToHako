import copy
import math
import random
import time

from ..game import Node, get_valid_action
from .base import BaseAgent


class UCTNode(Node):
    def __init__(self, parentNode, board, action, activePlayer):
        super().__init__(parentNode, board, action, activePlayer)

    def selectChild(self):
        selected = None
        bestValue = -1e5
        for child in self.children:
            uctValue = child.wins / child.visits + \
                math.sqrt(2 + math.log(self.visits) / child.visits)
            if (uctValue > bestValue):
                selected = child
                bestValue = uctValue

        return selected


class UCTAgent(BaseAgent):
    def __init__(self, name="uct", maxiterations=100, timelimit=1):
        super().__init__(name)
        self.maxiterations = maxiterations
        self.timelimit = timelimit

    def step(self, board, id_to_scores):
        root = UCTNode(None, board, None, self.player_id)
        blockSize = 50
        nodesVisited = 0

        start_time = time.time()

        for i in range(self.maxiterations):
            i += blockSize
            if time.time() - start_time > self.timelimit:
                break

            for _ in range(blockSize):
                node = copy.deepcopy(root)
                variantBoard = copy.deepcopy(board)
                variantScore = copy.deepcopy(id_to_scores)
                activePlayer = self.player_id

                while (len(node.unexamined) == 0 and len(node.children) > 0):
                    node = node.selectChild()
                    variantBoard, score = variantBoard.next_state(
                        node.action[0], node.action[1])
                    variantScore[activePlayer] += score
                    activePlayer *= -1

                if (len(node.unexamined) > 0):
                    j = random.randint(0, len(node.unexamined))
                    variantBoard, score = variantBoard.next_state(
                        node.unexamined[j][0], node.unexamined[j][1])
                    variantScore[activePlayer] += score
                    activePlayer *= -1
                    node.addChild(variantBoard, j, copy.deepcopy(variantScore))

                actions = get_valid_action(variantBoard)
                while (len(actions) > 0):
                    j = random.randint(0, len(actions))
                    variantBoard, score = variantBoard.next_state(
                        actions[j][0], actions[j][1])
                    variantScore[activePlayer] += score
                    activePlayer *= -1
                    nodesVisited += 1
                    actions = get_valid_action(variantBoard)

                while node is not None:
                    node.update(variantScore)
                    node = node.parentNode
