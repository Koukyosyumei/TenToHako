import json
import socket

from src.tentohako.game import Board


class Client:
    def __init__(self, agent, host_port):
        self.agent = agent
        self.host_port = host_port

        # connect to the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(("localhost", self.host_port))

        # receive id
        self._receive_uid()

    def _receive_uid(self):
        # send the id to the server
        msg_uid = self.sock.recv(4096)
        self.uid = json.loads(msg_uid)["uid"]
        print("uid: ", self.uid)

    def play(self):
        while True:
            try:
                # receive the state from the server
                msg_state = self.sock.recv(4096)
                state = json.loads(msg_state)
                board = Board(state["board_matrix"],
                              state["ncol"], state["nrow"])

                if board.is_done():
                    self.sock.close()
                    break

                if self.uid == state["next_player"]:
                    # choose the action
                    action = self.agent.step(board)
                    msg_action = json.dumps({"j": action[0],
                                             "i": action[1]}).encode()
                    self.sock.send(msg_action)

            except Exception as e:
                print(e)
                continue
