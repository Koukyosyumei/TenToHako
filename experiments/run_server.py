import argparse

from tentohako.socket import Server


def main(host_port, ncol, nrow, file_path):
    server = Server(host_port, ncol, nrow)
    server.set_clients()
    server.play()
    print("Result")
    print(server.id_to_scores)

    with open(file_path, "a") as f:
        f.write(f"{server.id_to_scores[1]}, {server.id_to_scores[-1]}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="host port",
                        type=int)
    parser.add_argument("-c", help="number of rows",
                        type=int)
    parser.add_argument("-r", help="number of columns",
                        type=int)
    parser.add_argument("-o", help="log file",
                        type=str)
    args = parser.parse_args()

    main(args.p, args.c, args.r, args.o)
