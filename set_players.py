from socket import *
import set_one_player

class player1(player0):
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def initialize(self, number, team_name, server_name, server_port):
        m_iNumber = number
        m_strTeamName = team_name
        m_strHostName = server_name
        




if __name__ == "__main__":
