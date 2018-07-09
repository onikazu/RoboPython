from socket import *


class Player0():
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.HOSTNAME = "localhost"
        self.PORT = 6000
        self.ADDRESS = gethostbyname(self.HOSTNAME)

    def send(self, command):
        to_byte_command = command.encode(encoding='utf_8')
        self.socket.sendto(to_byte_command, (self.ADDRESS, self.PORT))

    def receive(self):
        message = self.socket.recvfrom(4096)
        message = message.decode("utf_8")
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
