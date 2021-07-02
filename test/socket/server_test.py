import argparse
import os

from tentohako.socket import Server


def main(host_name, host_port, ncol, nrow, gif_path, log_path):
    server = Server(host_name, host_port, ncol, nrow)
    server.set_clients()
    server.play()
    server.save_plot(gif_path)

    with open(log_path, "a") as f:
        f.write(
            f"{server.id_to_name[1]},{server.id_to_scores[1]}," +
            f"{server.id_to_name[-1]},{server.id_to_scores[-1]}\n")

    os.remove(gif_path)
    os.remove(log_path)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="host name",
                        type=str)
    parser.add_argument("-p", help="host port",
                        type=int)
    parser.add_argument("-c", help="number of rows",
                        type=int)
    parser.add_argument("-r", help="number of columns",
                        type=int)
    parser.add_argument("--gp", help="path to gif",
                        type=str)
    parser.add_argument("--lp", help="path to log",
                        type=str)

    args = parser.parse_args()

    main(args.n, args.p, args.c, args.r, args.gp, args.lp)
