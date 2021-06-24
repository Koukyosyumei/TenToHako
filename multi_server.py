import json
import socket
import threading
import time

from src.tentohako.game import Board

NUM_PLAYER = 2
HOST = "localhost"
HOST_PORT = 8020

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, HOST_PORT))
sock.listen(NUM_PLAYER)


board = Board([], 3, 3)
board.initialize()
scores = [0]*NUM_PLAYER
clients = []


# 接続済みクライアントは読み込みおよび書き込みを繰り返す
def loop_handler(connection, address):
    global board
    while True:
        try:
            # check the status of the board
            if board.is_done():
                break

            # send the state to the client
            msg_state = json.dumps({"board_matrix": board.board_matrix,
                                    "ncol": board.ncol,
                                    "nrow": board.nrow,
                                    "done": board.is_done(),
                                    "score": 0}).encode()

            for value in clients:
                value[0].send(msg_state)

            msg_action = connection.recv(4096)
            for value in clients:
                if value[1][0] == address[0] and value[1][1] == address[1]:
                    action = json.loads(msg_action)
                    # generate the new state and culculate the score
                    board, score = board.next_state(action["j"], action["i"])

        except Exception as e:
            print(e)
            break


while True:
    try:
        # 接続要求を受信
        conn, addr = sock.accept()

    except KeyboardInterrupt:
        sock.close()
        exit()
        break
    # アドレス確認
    print("[アクセス元アドレス]=>{}".format(addr[0]))
    print("[アクセス元ポート]=>{}".format(addr[1]))
    print("\r\n")

    # 待受中にアクセスしてきたクライアントを追加
    clients.append((conn, addr))

    if len(clients) == NUM_PLAYER:
        print("starts game")
        # スレッド作成
        thread = threading.Thread(
            target=loop_handler, args=(conn, addr), daemon=True)
        # スレッドスタート
        thread.start()

        if board.is_done():
            break
