from src.tentohako.agent import RandomAgent
from src.tentohako.socket import Client

HOST_PORT = 8020


def main():
    agent = RandomAgent()
    client = Client(agent, HOST_PORT)
    client.play()


if __name__ == '__main__':
    main()
