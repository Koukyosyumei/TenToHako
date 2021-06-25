from src.tentohako.socket import Server

N_COL = 3
N_ROW = 3
HOST_PORT = 8020


def main():
    server = Server(HOST_PORT, N_COL, N_ROW)
    server.set_clients()
    server.play()


if __name__ == '__main__':
    main()
