import json
import socket
import threading

from src.tentohako.agent import RandomAgent
from src.tentohako.game import Board

HOST_PORT = 8020


agent = RandomAgent(0)

# connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", HOST_PORT))

board = None


def Handler(sock):
    while True:
        try:
            msg_state = sock.recv(4096)
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
            sock.send(msg_action)

        except Exception as e:
            continue


while (True):
    try:
        thread = threading.Thread(target=Handler, args=(sock,), daemon=True)
        thread.start()

        if board.is_done():
            break

    except Exception as e:
        continue
