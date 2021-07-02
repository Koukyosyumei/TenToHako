import copy
import math
import random
import time

from ..game import Node
from .base import BaseAgent


class UCTNode(Node):
    def __init__(self, parentNode, board, action, activePlayer,
                 id_to_scores, cpuct=0.3):
        super().__init__(parentNode, board, action, activePlayer, id_to_scores)
        self.cpuct = cpuct

    def addChild(self, board, index, id_to_scores):
        node = UCTNode(
            self, board, self.unexamined[index],
            self.activePlayer*-1, id_to_scores, cpuct=self.cpuct)
        del self.unexamined[index]
        self.children.append(node)
        return node

    def selectChild(self):
        selected = None
        bestValue = -1e5
        for child in self.children:
            uctValue = child.wins / (child.visits + 1) + \
                self.cpuct * \
                math.sqrt(2 * math.log(self.visits) / (child.visits + 1))
            if (uctValue > bestValue):
                selected = child
                bestValue = uctValue

        return selected


class UCTAgent(BaseAgent):
    def __init__(self, name="uct", maxiterations=1000, blocksize=50,
                 timelimit=1, cpuct=0.3):
        """An Agent which uses UCT (UCB applied to Trees)

        Args:
            name: the name of the agent
            maxiterations: the maximum number of iterations for searcing
            blocksize: block size for searcing
            timelimit: time-limit (s)
            cpuct: weight (parameter of UCT)

        Attributes:
            name: the name of the agent
            maxiterations: the maximum number of iterations for searcing
            blocksize: block size for searcing
            timelimit: time-limit (s)
            cpuct: weight
        """
        super().__init__(name)
        self.maxiterations = maxiterations
        self.timelimit = timelimit
        self.cpuct = cpuct
        self.blocksize = blocksize

    def step(self, board, id_to_scores):
        """Return the action based on the given board.

        Args:
            board: the instance of Board class which represents
                   the current board state.
            id_to_scores: dictionary whose keys are user id and values
                          are scores.

        Returns:
            picked_action: picked action
        """
        root = UCTNode(None, board, None, self.player_id,
                       id_to_scores, cpuct=self.cpuct)
        nodesVisited = 0

        start_time = time.time()

        for i in range(self.maxiterations):
            i += self.blocksize
            if time.time() - start_time > self.timelimit:
                break

            for _ in range(self.blocksize):
                node = root
                variantBoard = copy.deepcopy(board)
                variantScore = copy.deepcopy(id_to_scores)
                activePlayer = self.player_id

                while (len(node.unexamined) == 0 and len(node.children) > 0):
                    node = node.selectChild()
                    variantBoard, score = variantBoard.next_state(
                        node.action[0], node.action[1])
                    variantScore[str(activePlayer)] += score
                    activePlayer *= -1

                if (len(node.unexamined) > 0):
                    j = random.randint(0, len(node.unexamined)-1)
                    variantBoard, score = variantBoard.next_state(
                        node.unexamined[j][0], node.unexamined[j][1])
                    variantScore[str(activePlayer)] += score
                    activePlayer *= -1
                    node.addChild(variantBoard, j, variantScore)

                actions = self.get_valid_action(variantBoard)
                while (len(actions) > 0):
                    j = random.randint(0, len(actions)-1)
                    variantBoard, score = variantBoard.next_state(
                        actions[j][0], actions[j][1])
                    variantScore[str(activePlayer)] += score
                    activePlayer *= -1
                    nodesVisited += 1
                    actions = self.get_valid_action(variantBoard)

                if variantScore["1"] > variantScore["-1"]:
                    result = {1: 1, -1: 0}
                elif variantScore["1"] < variantScore["-1"]:
                    result = {1: 0, -1: 1}
                else:
                    result = {1: 0.5, -1: 0.5}
                while node is not None:
                    node.update(result, self.player_id)
                    node = node.parentNode

        print("num of visited nodes: ", nodesVisited)
        picked_action = root.mostVisitedChild().action
        return picked_action
