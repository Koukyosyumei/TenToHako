import argparse

from tentohako.agent import MinMaxAgent, QLearningAgent, RandomAgent, UCTAgent
from tentohako.socket import Client


def main(agent, host_name, host_port):
    client = Client(agent, host_name, host_port)
    client.play()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", help="the type of your agent",
                        type=str)
    parser.add_argument("-n", help="host name",
                        type=str, default="localhost")
    parser.add_argument("-p", help="host port",
                        type=int)
    parser.add_argument("-t", help="time limit when selecting the action",
                        type=int, default=2)
    parser.add_argument("-m", help="path to saved model",
                        type=str, default="../saved_models/qlearning_ncol_2_nrow_2_scoremin_1_scoremax_9_iterations_10000.pickle")
    args = parser.parse_args()

    if args.a == "r":
        agent = RandomAgent()
    elif args.a == "m":
        agent = MinMaxAgent()
    elif args.a == "u":
        agent = UCTAgent(timelimit=args.t)
    elif args.a == "q":
        agent = QLearningAgent()
        agent.load(args.m)
        agent.eval()
    else:
        agent = RandomAgent()

    main(agent, args.n, args.p)
