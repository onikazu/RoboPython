# ゾーンディフェンスを行う
import player9
import threading
from socket import *
import math


class Player10(player9.Player9, threading.Thread):
    def __init__(self):
        super(Player10, self).__init__()
        self.m_listCommand = []

    def getDirection(self, x0, y0, x1, y1):
        if abs(x1 - x0) < 0.1:
            if y1 - y0 > 0:
                return 90.0
            else:
                return -90.0
        else:
            return math.degrees(math.atan2(y1-y0, x1-x0))

    # @override
    def getCommandAsDefence(self, message, ballDist, ballDir):
        super().getCommandAsDefence(message, ballDist, ballDir)
        OUT_OF_RANGE = 999.0
        dist = self.getDistance(self.m_dDefenceX, self.m_dDefenceY, self.m_dX, self.m_dY)
        if dist < 2.0:
            return
        if self.m_dNeck == OUT_OF_RANGE:
            return
        dir = self.getDistance(self.m_dX, self.m_dY, self.m_dDefenceX, self.m_dDefenceY)
        moment = self.normalizeAngle(dir - self.m_dNeck)
        if abs(moment < 20.0):
            return "(dash 60)"
        elif abs(moment > 160.0):
            self.m_listCommand = []
            for _ in range(4):
                self.m_listCommand.append("(dash -40)")
            return "(dash -30)"
        else:
            self.m_listCommand = []
            for _ in range(6):
                self.m_listCommand.append("(dash 70)")
            return "(turn " + moment + ")"
        print("m_listCommand", self.m_listCommand)

    # @override
    def kick(self, message):
        goal = "(goal l)"
        if self.m_strSide.startswith("r"):
            goal = "(goal r)"
        if message.find(goal) > -1:
            return "(kick 100 180)"
        return super().kick(message)

    def play_1(self, message):
        # ボールが視界に無いとき
        print("p10", message)
        if not self.m_listCommand:
            super().play_1(message)

    # @override
    def analyzeMessage(self, message):
        # print("anamessage", message)
        super().analyzeMessage(message)
        if message.startswith("(sense"):
            if self.m_listCommand:
                command = self.m_listCommand.pop(0)
                print(self.m_listCommand)
                self.send(command)


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
