# ボール位置の絶対座標を用いる
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
            for i in range(4):
                self.m_listCommand.append("(dash -40)")
            return "(dash -30)"
        else:
            self.m_listCommand = []
            for i in range(6):
                self.m_listCommand.append("(dash 70)")
            return "(turn " + moment + ")"

    # @override
    def kick(self, message):
        goal = "(goal l)"
        if self.m_strSide.startswith("r"):
            goal = "(goal r)"
        if message.find(goal) > -1:
            return "(kick 100 180)"
        return super().kick(message)

    def play(self, message, ballDist=None, ballDir=None):
        # ボールが視界に無いとき
        if ballDist is None and ballDir is None:
            if len(self.m_listCommand) == 0:
                # 初期化
                if self.checkInitialMode():
                    self.setKickOffPosition()
                    command = "(move " + str(self.m_dKickOffX) + " " \
                        + str(self.m_dKickOffY) + ")"
                    self.send(command)
                # 初期ではない
                else:
                    message = message.replace("B", "b")
                    ball = self.getObjectMessage(message, "((b")
                    # print("メッセージ", message)
                    # ボールが見えるようになった
                    if ball.startswith("((b"):
                        ballDist = self.getParam(ball, "(ball)", 1)
                        # ここがおかしい
                        ballDir = self.getParam(ball, "(ball)", 2)
                        # print("ballDir", ballDir)
                        # ボールが見えているときのplayへ
                        self.play(message, ballDist, ballDir)
                    # 見えない
                    else:
                        command = "(turn 30)"
                        self.send(command)
                        # print("a:", command)
            # ボールが見えているときのplay
        else:
            command = ""
            # 体の正面にある
            if abs(ballDir) < 20.0:
                # そして近い
                if ballDist < 1.0:
                    command = self.kick(message)
                    print("b", command)
                # 遠い
                elif self.checkNearest(message, ballDist, ballDir):
                    command = "(dash 80)"
                    print("d", command)
                else:
                    command = self.getCommandAsDefence(message, ballDist, ballDir)
            # 体の正面にはない　ここがおかしいと見て間違いない
            else:
                command = "(turn " + str(ballDir) + ")"
                print("c", command)
            self.send(command)

    # @override
    def analyzeMessage(self, message):
        super().analyzeMessage(message)
        if message.startswith("(sense"):
            if len(self.m_listCommand) > 0:
                command = str(self.m_listCommand.pop(0))
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
