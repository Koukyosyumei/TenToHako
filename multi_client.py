import argparse
import json
import random
import socket
import sys
import threading

from src.tentohako.agent import RandomAgent
from src.tentohako.game import Board

HOST_PORT = 8020

uid = random.randint(0, 10000)
agent = RandomAgent(uid)

# connect to the server
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("localhost", HOST_PORT))
# send the id to the server
sock.send(json.dumps(uid).encode())

board = None


def Handler(sock):
    while True:
        try:
            msg_state = sock.recv(4096)
            state = json.loads(msg_state)
            board = Board(state["board_matrix"], state["ncol"], state["nrow"])

            if board.is_done():
                sock.close()
                sys.exit()
                break

            if uid == state["next_player"]:
                # choose the action
                action = agent.step(board)
                print("send action: ", action, "from: ", uid)
                msg_action = json.dumps({"j": action[0],
                                         "i": action[1]}).encode()
                sock.send(msg_action)

        except Exception as e:
            continue


while (True):
    try:
        thread = threading.Thread(target=Handler, args=(sock,), daemon=True)
        thread.start()

    except Exception as e:
        continue
