import argparse

from tentohako.agent import MinMaxAgent, QLearningAgent, RandomAgent, UCTAgent
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
    elif args.a == "q":
        agent = QLearningAgent()
        agent.load(
            "../saved_models/qlearning_ncol_3_nrow_3_scoremin_1_scoremax_9_iterations_3000.pickle")
        agent.eval()
    else:
        agent = RandomAgent()

    main(agent, args.p)
