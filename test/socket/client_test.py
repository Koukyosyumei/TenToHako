import argparse

from tentohako.agent import RandomAgent
from tentohako.socket import Client


def main(host_port):
    agent = RandomAgent()
    client = Client(agent, host_port)
    client.play()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", help="host port",
                        type=int)
    args = parser.parse_args()

    main(args.p)
