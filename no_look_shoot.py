import nearest_recog
import threading
from socket import *
import math


class Player7(nearest_recog.Player6, threading.Thread):
    def __init__(self):
        super(Player7, self).__init__()

    def normalizeAngle(self, angle):
        if abs(angle) > 720.0:
            print("error about angle")
        while angle > 180.0:
            angle -= 360.0
        while angle < -180:
            angle += 360.0
        return angle

    def getNeckDir(self, message):
        OUT_OF_RANGE = 999.0
        index0 = message.find("((l")
        lineName = ""
        line = ""
        lineDist = -1 * OUT_OF_RANGE
        lineDir = -1 * OUT_OF_RANGE
        while index0 > -1:
            index1 = message.find(")", index0+3)
            lineName = message[index0+1:index1+1]
            line = "(" + lineName
            index2 = message.find(")", index1+1)
            line += message[index1+1:index2+1]
            dist = self.getParam(line, lineName, 1)
            dir = self.getParam(line, lineName, 2)
            if dist > lineDist:
                lineDist = dist
                lineDir = dir
            index0 = message.find("((l", index0+3)
        if lineDist == OUT_OF_RANGE:
            return OUT_OF_RANGE

        playerNeck = OUT_OF_RANGE
        if lineName.startswith("(line b)"):
            if 0 < lineDir and lineDir <= 90:
                playerNeck = 180 - lineDir
            else:
                playerNeck = -lineDir
        elif lineName.startswith("(line t)"):
            if 0 < lineDir and lineDir <= 90:
                playerNeck = -lineDir
            else:
                playerNeck = -180 - lineDir
        elif lineName.startswith("(line l)"):
            if 0 < lineDir and lineDir <= 90:
                playerNeck = -90 - lineDir
            else:
                playerNeck = 90 - lineDir
        elif lineName.startswith("(line r)"):
            if 0 < lineDir and lineDir <= 90:
                playerNeck = 90 - lineDir
            else:
                playerNeck = -90 - lineDir
        return playerNeck

    # @override
    def kick(self, message):
        print("player7 into kick section")
        targetGoal = ""
        if self.m_strSide.startswith("r"):
            targetGoal = "(goal l)"
        else:
            targetGoal = "(goal r)"

        index0 = message.find(targetGoal)
        # ゴールが見える
        if index0 > -1:
            print("i can look goal!!")
            goalDist = 0.0
            goalDir = 0.0
            goalDist = self.getParam(message, targetGoal, 1)
            goalDir = self.getParam(message, targetGoal, 2)
            return "(kick 100 " + str(goalDir) + ")"
        else:
        # ゴールが見えない
            print("i cant look goal")
            neckDir = self.getNeckDir(message)
            attackDir = 0.0
            if self.m_strSide.startswith("r"):
                attackDir = 180.0
            kickDir = self.normalizeAngle(attackDir - neckDir)
            if self.m_strPlayMode.startswith("play_on"):
                return "(kick 30 " + str(kickDir) + ")"
            else:
                return "(kick 100 " + str(kickDir) + ")"


if __name__ == "__main__":
    player6s = []
    for i in range(11):
        p6 = nearest_recog.Player6()
        player6s.append(p6)
        teamname = "p6s"
        player6s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player6s[i].start()
    player7s = []
    for i in range(11):
        p7 = Player7()
        player7s.append(p7)
        teamname = "p7s"
        player7s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player7s[i].start()

    print("試合登録完了")