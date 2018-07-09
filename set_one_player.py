from socket import *


class Player0():
    HOSTNAME = "localhost"
    PORT = 6000
    ADDRESS = gethostbyname(HOSTNAME)

    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def send(self, command):
        to_byte_command = command.encode(encoding='utf_8')
        self.socket.sendto(to_byte_command, (ADDRESS, PORT))

    def receive(self):
        data, addr = self.socket.recvfrom(4096)
        # print(data)


if __name__ == "__main__":
    player = Player0()
    command = "(init teamKazu (goalie))"
    player.send(command)
    print("送信：", command)
    message = player.receive()
    print("受信：", message)
    print("試合登録完了")
    while True:
        message = player.receive()
