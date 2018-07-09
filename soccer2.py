HOSTNAME = "localhost"
PORT = 6000


class Player():
    def __init__(self):
        self.socket = socket(AF_INET, SOCK_DGRAM)

    def send(self, command):
        socket.sendto(command, (ADDRESS, PORT))
        if msg == ".":
            break

    def receive(self):
        data, addr = client.recvfrom(4096)
        print(data)


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
