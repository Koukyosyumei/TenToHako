import json
import socket
import time

from src.tentohako.game import Board

NUM_MAXPLAYER = 2
HOST_PORT = 8020

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", HOST_PORT))
sock.listen(NUM_MAXPLAYER)


board = Board([], 3, 3)
board.initialize()
scores = [0]*NUM_MAXPLAYER

clients = []

# connect to the client
clientsocket, address = sock.accept()
clients.append([clientsocket, address])
print('Connection from {} is established on {}'.
      format(address, time.time()))

while True:

    # send the state to the client
    msg_state = json.dumps({"board_matrix": board.board_matrix,
                            "ncol": board.ncol,
                            "nrow": board.nrow,
                            "done": board.is_done(),
                            "score": 0}).encode()
    clientsocket.sendall(msg_state)

    if board.is_done():
        break

    # receive the picked action from the server
    msg_action = clientsocket.recv(1024)
    action = json.loads(msg_action)

    # generate the new state and culculate the score
    board, score = board.next_state(action["j"], action["i"])
