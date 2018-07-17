import player12
import threading
from socket import *
import math


class Player13(player12.Player12, threading.Thread):
    def __init__(self):
        super(Player13, self).__init__()
        self.dash_power_rate = 0.006
        self.player_decay = 0.4

    def predictDashCommand(self, i):
        command = self.m_strCommand[i]
        if command.startswith("(dash"):
            dash_power = self.getParam(command, "dash", 1)
            p = math.pi
            rad = self.m_dBody[i] * math.pi / 180
            ax = dash_power * self.dash_power_rate * math.cos(rad)
            ay = dash_power * self.dash_power_rate * math.sin(rad)
            self.m_dAX[i] = ax
            self.m_dAY[i] = ay

        next = (i + 1) % self.GAME_LENGTH
        self.m_dVX[next] = (self.m_dVX + self.m_dAX) * self.player_decay
        self.m_dVY[next] = (self.m_dVY + self.m_dAY) * self.player_decay
        self.m_dX[next] = self.m_dX + self.m_dVX[i] + self.m_dAX[i]
        self.m_dY[next] = self.m_dY + self.m_dVY[i] + self.m_dAY[i]
        self.m_dAX[next] = 0.0
        self.m_dAY[next] = 0.0

    def predict(self, start, end):
        super().predict(start, end)
        # 予測確認

    def play_0(self):
        super().play_0()
        if self.m_strPlayMode.startswith("kick_off"):
            command = ""
            if self.m_iTime % 10 < 5:
                command = "(dash 100)"
            else:
                command = "(dash -100)"
            self.m_strCommand[self.m_iTime] = command

    def analyzeServerParam(self, message):
        super().analyzeServerParam(message)
        self.player_decay = self.getParam(self.m_strServerParam, "player_decay", 1)
        self.dash_power_rate = self.getParam(self.m_strServerParam, "dash_power_rate", 1)


if __name__ == "__main__":
    player13s = []
    for i in range(11):
        p13 = Player13()
        player13s.append(p13)
        teamname = "p13s"
        player13s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player13s[i].start()

    print("試合登録完了")


