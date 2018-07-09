from socket import *
import threading
import set_one_player.Player0


class Player1(Player0, threading.Thread):
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def initialize(self, number, team_name, server_name, server_port):
        m_iNumber = number
        m_strTeamName = team_name
        m_strHostName = server_name
        if m_iNumber == 1:
            command = "(init " + m_strTeamName + "(goalie))"
        else:
            command = "(init " + m_strTeamName + ")"
        send(command)

    def run(self):
        while True:
            message = receive()
            analyzeMessage(message)

    def analyzeInitialMessage(self, message):
        index0 = message.index(" ")
        index1 = message.index(" ", index0 + 1)
        index2 = message.index(" ", index1 + 1)
        index3 = message.index(" ", index2 + 1)

        m_strSide = message[index0+1:index1]
        m_iNumber = int(message[index1+1:index2])
        m_strPlayMode = message[index2+1:index3]

    def analyzeMessage(self, message):
        if message.startswith("(init"):
            analyzeInitialMessage(message)


if __name__ == "__main__":
    players = []
    for i in range(11):
        players.append(Player1())
        players[i].initialize(i+1, "kazu", "localhost", 6000)
        players[i].start()
