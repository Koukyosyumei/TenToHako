import json
import random
import socket

from src.tentohako.agent import RandomAgent
from src.tentohako.game import Board

HOST_PORT = 8020

# connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", HOST_PORT))

# send the id to the server
msg_uid = sock.recv(4096)
uid = json.loads(msg_uid)["uid"]
print("uid: ", uid)
agent = RandomAgent(uid)

while True:
    try:
        # receive the state from the server
        msg_state = sock.recv(4096)
        state = json.loads(msg_state)
        board = Board(state["board_matrix"], state["ncol"], state["nrow"])

        if board.is_done():
            sock.close()
            break

        if uid == state["next_player"]:
            # choose the action
            action = agent.step(board)
            msg_action = json.dumps({"j": action[0],
                                     "i": action[1]}).encode()
            sock.send(msg_action)

    except Exception as e:
        print(e)
        continue
