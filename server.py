import json
import socket
import time

from src.tentohako.game import Board

NUM_PLAYER = 2
HOST_PORT = 8020

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(("localhost", HOST_PORT))
sock.listen(NUM_PLAYER)


board = Board([], 3, 3)
board.initialize()
print(board.board_to_string())

clients = []

# connect to the client
clientsocket_1, address_1 = sock.accept()
clients.append([clientsocket_1, address_1])
print('Connection from {} is established on {}'.
      format(address_1, time.time()))
clientsocket_1.sendall(json.dumps({"uid": 1}).encode())

clientsocket_2, address_2 = sock.accept()
clients.append([clientsocket_2, address_2])
print('Connection from {} is established on {}'.
      format(address_2, time.time()))
clientsocket_2.sendall(json.dumps({"uid": -1}).encode())

id_to_clients = {1: clientsocket_1, -1: clientsocket_2}
id_to_scores = {1: 0, -1: 0}

next_player = 1
step = 1


print("Game Starts !")
while True:
    print(f"step {step}")
    # send the state to the client
    msg_state = json.dumps({"board_matrix": board.board_matrix,
                            "ncol": board.ncol,
                            "nrow": board.nrow,
                            "done": board.is_done(),
                            "score": id_to_scores,
                            "next_player": next_player}).encode()
    clientsocket_1.sendall(msg_state)
    clientsocket_2.sendall(msg_state)

    # if the game is over, terminate the program
    if board.is_done():
        break

    # receive the picked action from the server
    msg_action = id_to_clients[next_player].recv(1024)
    action = json.loads(msg_action)

    # generate the new state and culculate the score
    board, score = board.next_state(action["j"], action["i"])
    id_to_scores[next_player] += score

    print(f"uid {next_player} get {score} points")

    # switch the player
    next_player *= -1

    # incriment the step
    step += 1

    print(board.board_to_string())
    print("-------------------------------------")


# thr result of the game
print("Finish !")
print(id_to_scores)
