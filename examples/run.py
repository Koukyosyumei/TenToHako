import argparse
import subprocess

name = "localhost"
port = 8020
command_client_base = "python run_client.py"
command_server_base = "python run_server.py"


def run(num_games, ncols, nrows, agent_1, agent_2, vis, log_path, gif_name):
    for i in range(1, num_games + 1):
        command_client_args_1 = f" -n {name} -p {port} -a {agent_1}"
        command_client_args_2 = f" -n {name} -p {port} -a {agent_2}"
        command_server_args = f" -n {name} -p {port} -c\
             {ncols} -r {nrows} --gp {gif_name}_{i}.gif --lp {log_path}"
        _ = subprocess.Popen(command_client_base + command_client_args_1)
        _ = subprocess.Popen(command_client_base + command_client_args_2)
        p = subprocess.Popen(command_server_base + command_server_args)
        p.wait()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-n", help="number of games", type=int, default=1)
    parser.add_argument("-c", help="number of rows", type=int, default=3)
    parser.add_argument("-r", help="number of columns", type=int, default=3)
    parser.add_argument(
        "--a1",
        help="agent type r: random, m: minmax,\
                        u: uct, q: q-learning",
        type=str,
        default="r",
    )
    parser.add_argument(
        "--a2",
        help="agent type r: random, m: minmax,\
                        u: uct, q: q-learning",
        type=str,
        default="r",
    )
    parser.add_argument("-v", help="plot (1) or not (0)", type=int, default=1)
    parser.add_argument(
        "--lp", help="path to the log file", type=str, default="log.txt"
    )
    parser.add_argument(
        "--gp",
        help="name of the gif file,\
                         this program will generate the gif file\
                         like <gp>_<number_of_game>.gif",
        type=str,
        default="experiment",
    )
    args = parser.parse_args()
    run(args.n, args.c, args.r, args.a1, args.a2, args.v, args.lp, args.gp)
