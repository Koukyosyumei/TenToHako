import json
import socket

from ..game import Board


class Client:
    def __init__(self, agent, host_name, host_port):
        """Class which represents the participant of the game.

        Args:
            agent: class which defines the agent.
                   This class should have member function `step`,
                   which takes the instance of the Board class as an argument.
            host_name: the host name
            host_port: port number of the host server.

        Attributes:
            agent: class which defines the agent.
                   This class should have member function `step`,
                   which takes the instance of the Board class as an argument.
            host_port: port number of the host server.
            sock: socket which connects this client and the host server.
            uid: the id of the client.
        """
        self.agent = agent
        self.host_name = host_name
        self.host_port = host_port

        # connect to the server
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host_name, self.host_port))

        # send name
        self._send_name()

        # receive id
        self._receive_uid()

    def _send_name(self):
        """Send the user name to the server"""
        msg_name = json.dumps(self.agent.name).encode()
        self.sock.send(msg_name)

    def _receive_uid(self):
        """Receive the id of the client from the host server"""
        # send the id to the server
        msg_uid = self.sock.recv(4096)
        self.uid = json.loads(msg_uid)["uid"]
        print("uid: ", self.uid)
        self.agent.set_player_id(self.uid)

    def play(self):
        """Play the game"""
        while True:
            try:
                # receive the state from the server
                msg_state = self.sock.recv(4096)
                state = json.loads(msg_state)
                board = Board(state["board_matrix"], state["ncol"], state["nrow"])

                if board.is_done():
                    self.sock.close()
                    break

                if self.uid == state["next_player"]:
                    # choose the action
                    action = self.agent.step(board, state["score"])
                    msg_action = json.dumps({"j": action[0], "i": action[1]}).encode()
                    self.sock.send(msg_action)

            except Exception as e:
                print(e)
                continue
