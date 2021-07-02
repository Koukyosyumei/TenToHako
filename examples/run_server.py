import argparse

from tentohako.socket import Server


def main(host_name, host_port, ncol, nrow, log_path, visualize, gif_path):
    server = Server(host_name, host_port, ncol, nrow)
    server.set_clients()
    server.play()
    if visualize == 1:
        server.save_plot(gif_path)
    print("Result")
    print(server.id_to_scores)

    with open(log_path, "a") as f:
        f.write(
            f"{server.id_to_name[1]},{server.id_to_scores[1]}," +
            f"{server.id_to_name[-1]},{server.id_to_scores[-1]}\n")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="host name",
                        type=str, default="localhost")
    parser.add_argument("-p", help="host port",
                        type=int)
    parser.add_argument("-c", help="number of rows",
                        type=int)
    parser.add_argument("-r", help="number of columns",
                        type=int)
    parser.add_argument("-v", help="plot (1) or not (0)",
                        type=int, default=1)
    parser.add_argument("--lp", help="log file",
                        type=str)
    parser.add_argument("--gp", help="gif file",
                        type=str)

    args = parser.parse_args()

    main(args.n, args.p, args.c, args.r, args.lp, args.v, args.gp)
