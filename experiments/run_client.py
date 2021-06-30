import argparse

from tentohako.agent import MinMaxAgent, RandomAgent, UCTAgent
from tentohako.socket import Client


def main(agent, host_port):
    client = Client(agent, host_port)
    client.play()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help="the type of your agent",
                        type=str)
    parser.add_argument("-p", help="host port",
                        type=int)
    args = parser.parse_args()

    if args.a == "r":
        agent = RandomAgent()
    elif args.a == "m":
        agent = MinMaxAgent()
    elif args.a == "u":
        agent = UCTAgent(timelimit=2)
    else:
        agent = RandomAgent()

    main(agent, args.p)
