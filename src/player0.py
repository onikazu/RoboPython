from socket import *


class Player0():
    def __init__(self):
        # UDPはSOCK_DGRAM
        # TCPIPはSOCK_STREAM
        # self.socket = socket(AF_INET, SOCK_DGRAM)
        self.socket = socket(AF_INET, SOCK_STREAM)
        self.HOSTNAME = "localhost"
        self.PORT = 6000
        self.ADDRESS = gethostbyname(self.HOSTNAME)

    def send(self, command):
        if len(command) == 0:
            return
        to_byte_command = command.encode(encoding='UTF-8')
        self.socket.sendto(to_byte_command, (self.ADDRESS, self.PORT))

    def receive(self):
        message, arr = self.socket.recvfrom(4096)
        message = message.decode("UTF-8")
        return message
        # print(data)


if __name__ == "__main__":
    player = Player0()
    command = "(init teamKazu (goalie))"
    player.send(command)
    print("send:", command)
    message = player.receive()
    print("receive:", message)
    print("completed")
    while True:
        message = player.receive()
