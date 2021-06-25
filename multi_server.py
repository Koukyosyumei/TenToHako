import json
import socket
import threading

from src.tentohako.game import Board

NUM_PLAYER = 2
HOST = "localhost"
HOST_PORT = 8020

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((HOST, HOST_PORT))
sock.listen(NUM_PLAYER)


board = Board([], 3, 3)
board.initialize()
uids = []
scores = {}
address_to_uid = {}
uid_to_address = {}
clients = []
next_player = None


# 接続済みクライアントは読み込みおよび書き込みを繰り返す
def loop_handler(connection, address):
    global board, next_player
    if len(clients) == NUM_PLAYER:
        print("starts game")
        while True:
            try:
                # check the status of the board
                print(board.board_to_string())

                if board.is_done():
                    sock.close()
                    exit()
                    break

                print(uid_to_address[next_player], address)

                print("receive action from: ",
                      f"{address[0]}:{address[1]}")

                if uid_to_address[next_player] == f"{address[0]}:{address[1]}":
                    # send the state to the client
                    msg_state = json.dumps({"board_matrix": board.board_matrix,
                                            "ncol": board.ncol,
                                            "nrow": board.nrow,
                                            "done": board.is_done(),
                                            "score": 0,
                                            "next_player": next_player}).encode()

                    # send the state to all clients
                    for value in clients:
                        value[0].send(msg_state)

                    print("match")
                    msg_action = connection.recv(4096)
                    action = json.loads(msg_action)
                    # generate the new state and culculate the score
                    board, score = board.next_state(
                        action["j"], action["i"])
                    scores[next_player] = score

                    print(next_player)
                    print(action)
                    print(score)

                    print("----")

                    if NUM_PLAYER == uids.index(next_player)+1:
                        next_player = uids[0]
                    else:
                        next_player = uids[uids.index(next_player)+1]
                else:
                    print("mismatch")

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

    # receive the id of the client
    msg_uid = conn.recv(4096)
    uid = json.loads(msg_uid)

    # set the client to the dictionaries
    uids.append(uid)
    scores[uid] = 0
    address_to_uid[f"{addr[0]}:{addr[1]}"] = uid
    uid_to_address[uid] = f"{addr[0]}:{addr[1]}"

    # set the initial player
    next_player = uids[0]

    # スレッド作成
    thread = threading.Thread(
        target=loop_handler, args=(conn, addr), daemon=True)
    # スレッドスタート
    thread.start()
