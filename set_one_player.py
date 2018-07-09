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
        data, addr = self.socket.recvfrom(4096)
        # print(data)


if __name__ == "__main__":
    player = Player()
    command = "(init teamKazu (goalie))"
    player.send(command)
    print("送信：", command)
    message = player.receive()
    print("受信：", message)
    print("試合登録完了")
    while True:
        message = player.receive()
