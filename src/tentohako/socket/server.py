import json
import socket
import time

from src.tentohako.game import Board


class Server:
    def __init__(self, port,
                 ncol, nrow, num_player=2,
                 score_min=1, score_max=9):
        self.port = port
        self.num_player = num_player

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(("localhost", port))
        self.sock.listen(num_player)

        self.board = Board([], ncol, nrow, score_min=score_min,
                           score_max=score_max)
        self.board.initialize()

        self.user_ids = []
        self.id_to_address = {}
        self.id_to_clients = {}
        self.id_to_scores = {}
        self.next_player = None
        self.step = 0

    def set_clients(self):
        self.user_ids = [1, -1]
        for i in range(self.num_player):
            clientsocket, address = self.sock.accept()
            self.id_to_clients[self.user_ids[i]] = clientsocket
            self.id_to_address[self.user_ids[i]] = address
            self.id_to_scores[self.user_ids[i]] = 0
            print('Connection from {} is established on {}'.
                  format(address, time.time()))

            clientsocket.sendall(json.dumps(
                {"uid": self.user_ids[i]}).encode())

    def _send_current_state(self):
        # send the state to the client
        msg_state = json.dumps({"board_matrix": self.board.board_matrix,
                                "ncol": self.board.ncol,
                                "nrow": self.board.nrow,
                                "done": self.board.is_done(),
                                "score": self.id_to_scores,
                                "next_player": self.next_player}).encode()
        for idx in self.user_ids:
            self.id_to_clients[idx].sendall(msg_state)

    def _receive_and_apply_picked_actions(self):
        # receive the picked action from the server
        msg_action = self.id_to_clients[self.next_player].recv(4096)
        action = json.loads(msg_action)

        # generate the new state and culculate the score
        self.board, score = self.board.next_state(action["j"], action["i"])
        self.id_to_scores[self.next_player] += score

        print(f"uid {self.next_player} get {score} points")

    def play(self, steps_limit=1e5):
        self.next_player = 1
        while self.step < steps_limit:

            self._send_current_state()

            # if the game is over, terminate the program
            if self.board.is_done():
                break
            self._receive_and_apply_picked_actions()

            # switch the player
            self.next_player *= -1

            # incriment the step
            self.step += 1

            print(self.board.board_to_string())
            print("-------------------------------------")
