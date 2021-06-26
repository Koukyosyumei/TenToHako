import argparse

from tentohako.agent import MinMaxAgent, RandomAgent
from tentohako.socket import Client

HOST_PORT = 8020


def main(agent):
    client = Client(agent, HOST_PORT)
    client.play()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help="the type of your agent",
                        type=str)
    args = parser.parse_args()

    if args.a == "r":
        agent = RandomAgent()
    elif args.a == "m":
        agent = MinMaxAgent()
    else:
        agent = RandomAgent()

    main(agent)
