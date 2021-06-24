import json
import socket

from src.tentohako.agent import RandomAgent
from src.tentohako.game import Board

HOST_PORT = 8020


agent = RandomAgent(0)

# connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", HOST_PORT))

while True:
    try:
        # receive the state from the server
        msg_state = sock.recv(1024)
        state = json.loads(msg_state)
        board = Board(state["board_matrix"], state["ncol"], state["nrow"])
        print(board.board_to_string())

        if board.is_done():
            break

        # choose the action
        action = agent.step(board)
        print(action)
        msg_action = json.dumps({"j": action[0],
                                 "i": action[1]}).encode()
        sock.sendall(msg_action)

    except Exception as e:
        print(e)
        continue
