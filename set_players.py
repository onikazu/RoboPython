from socket import *
import threading


class Player1(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.HOSTNAME = "localhost"
        self.PORT = 6000
        self.ADDRESS = gethostbyname(self.HOSTNAME)

    def send(self, command):
        to_byte_command = command.encode(encoding='utf_8')
        self.socket.sendto(to_byte_command, (self.ADDRESS, self.PORT))

    def receive(self):
        data, addr = self.socket.recvfrom(4096)
        # print(data)

    def initialize(self, number, team_name, server_name, server_port):
        m_iNumber = number
        m_strTeamName = team_name
        m_strHostName = server_name
        if m_iNumber == 1:
            command = "(init " + m_strTeamName + "(goalie))"
        else:
            command = "(init " + m_strTeamName + ")"
        self.send(command)

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
        p = Player1()
        players.append(p)
        players[i].initialize(i+1, "kazu", "localhost", 6000)
        players[i].start()
