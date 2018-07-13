# ゾーンディフェンスを行う
import player9
import threading
from socket import *
import math


class Player10(player9.Player9, threading.Thread):
    def __init__(self):
        super(Player10, self).__init__()



if __name__ == "__main__":
    player10s = []
    for i in range(11):
        p10 = Player10()
        player10s.append(p10)
        teamname = "p10s"
        player10s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player10s[i].start()
    player9s = []
    for i in range(11):
        p9 = player9.Player9()
        player9s.append(p9)
        teamname = "p9s"
        player9s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player9s[i].start()

    print("試合登録完了")
