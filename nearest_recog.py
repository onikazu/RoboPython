import kick
import threading
from socket import *
import math


class Player6(kick.Player5, threading.Thread):
    def __init__(self):
        super(Player6, self).__init__()

    # 自分がボールに一番近いかどうかの判断
    def checkNearest(self, message, ballDist, ballDir):
        teamname = "(player" + self.m_strTeamName
        player = self.getObjectMessage(message, "((p")
        index0 = player.find(teamname, 0)
        while index0 > -1:
            index1 = player.find(")", index0)
            index2 = player.find(" ", index1 + 1)
            index3 = player.find(" ", index2 + 1)
            index4 = player.find(" ", index3 + 1)
            index5 = player.find(")", index3 + 1)
            if index5 < index4 or index4 == -1:
                index4 = index5
            playerDist = float(player[index2:index3])
            playerDir = float(player[index3:index4])
            A = ballDist
            B = playerDist
            rad = math.pi / 180.0 * (playerDir - ballDir)
            dist = math.sqrt(A * A + B * B - 2 * A * B * math.cos(rad))
            if dist < ballDist:
                return False
                print("judged")
            index0 = player.find(teamname, index0 + len(teamname))
        return True

    def getCommandAsDefence(self, message, ballDist, ballDir):
        command = ""
        goal = "(goal l)"
        if  self.m_strSide.startswith("r"):
            goal = "(goal r)"
        if message.find(goal) > -1:
            goalDist = self.getParam(message, goal, 1)
            if goalDist > 50.0:
                command = "(dash 80)"
        return command

    def play(self, message, ballDist=None, ballDir=None):
        # ボールが視界に無いとき
        if ballDist is None and ballDir is None:
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
                print("メッセージ", message)
                # ボールが見えるようになった
                if ball.startswith("((b"):
                    ballDist = self.getPram(ball, "(ball)", 1)
                    # ここがおかしい
                    ballDir = self.getPram(ball, "(ball)", 2)
                    print("ballDir", ballDir)
                    # ボールが見えているときのplayへ
                    self.play(message, ballDist, ballDir)
                # 見えない
                else:
                    command = "(turn 30)"
                    self.send(command)
                    print("a:", command)
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


if __name__ == "__main__":
    player6s = []
    for i in range(11):
        p6 = Player6()
        player6s.append(p6)
        teamname = "p6s"
        player6s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player6s[i].start()
    player5s = []
    for i in range(11):
        p5 = kick.Player5()
        player5s.append(p5)
        teamname = "p5s"
        player5s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player5s[i].start()

    print("試合登録完了")
