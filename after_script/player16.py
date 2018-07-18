import player15
import threading
from socket import *
import math


class Player16(player15.Player15, threading.Thread):
    def __init__(self):
        super(Player16, self).__init__()
        self.inertia_moment = 5.0
        self.maxneckang = 90.0
        self.minneckang = -90.0
        self.m_dHeadAngle = []
        self.OUT_OF_RANGE = 999.9
        for _ in range(self.GAME_LENGTH):
            self.m_dHeadAngle.append(0.0)

    def analyzePhysicalMessage(self, message):
        super().analyzePhysicalMessage(message)
        print("p16:self.m_dNeck[self.m_iTime]:", self.m_dNeck[self.m_iTime])
        print("p16:self.OUT_OF_RANGE:", self.OUT_OF_RANGE)
        if self.m_dNeck[self.m_iTime] == self.OUT_OF_RANGE:
            return

        speed = self.getParam(message, "speed", 1)
        speed_angle = self.getParam(message, "speed", 2)
        rad = self.normalizeAngle(self.m_dNeck[self.m_iTime] + speed_angle) * math.pi / 180.0
        vx = speed * math.cos(rad)
        vy = speed * math.sin(rad)
        self.m_dVX[self.m_iTime] = vx
        self.m_dVY[self.m_iTime] = vy
        head_angle = self.getParam(message, "head_angle", 1)
        body_angle = self.normalizeAngle(self.m_dNeck[self.m_iTime] - head_angle)
        self.m_dHeadAngle[self.m_iTime] = head_angle
        self.m_dBody[self.m_iTime] = body_angle

    def predictTurnCommand(self, i):
        next = (i + 1) % self.GAME_LENGTH
        if self.m_dNeck[i] == self.OUT_OF_RANGE:
            return
        command = self.m_strCommand[i]
        if command.startswith("(turn"):
            moment = self.getParam(command, "turn", 1)
            vx = self.m_dVX[i]
            vy = self.m_dVY[i]
            speed = math.sqrt(vx * vx + vy * vy)
            turn_angle = moment / (1 + self.inertia_moment * speed)
            self.m_dNeck[next] = self.normalizeAngle(self.m_dNeck[i] + turn_angle)
            self.m_dBody[next] = self.normalizeAngle(self.m_dBody[i] + turn_angle)
        else:
            self.m_dNeck[next] = self.m_dNeck[i]
            self.m_dBody[next] = self.m_dBody[i]
        index0 = command.find("(turn_neck")
        if index0 > -1:
            index1 = command.find(" ", index0+9)
            index2 = command.find(")", index1+1)
            angle = float(str(command[index1:index2]))
            print("p16:angle:", angle)
            head_angle = self.normalizeAngle(self.m_dNeck[i] - self.m_dBody[i])
            if self.maxneckang < head_angle + angle:
                self.m_dNeck[next] = self.normalizeAngle(self.m_dBody[i] + self.maxneckang)
            elif self.minneckang > head_angle + angle:
                self.m_dNeck[next] = self.normalizeAngle(self.m_dBody[i] + self.minneckang)
            else:
                self.m_dNeck[next] = self.normalizeAngle(self.m_dNeck[next] + angle)

    def predict(self, start, end):
        super().predict(start, end)

    def analyzePlayerType(self, message):
        super().analyzePlayerType(message)
        type = self.m_strPlayerType[self.m_iPlayerType]
        self.inertia_moment = self.getParam(type, "inertia_moment", 1)

    def analyzeServerParam(self, message):
        super().analyzeServerParam(message)
        self.maxneckang = self.getParam(message, "maxneckang", 1)
        self.minneckang = self.getParam(message, "minneckang", 1)

    def play_0(self):
        super().play_0()
        if self.m_strPlayMode.startswith("kick_off"):
            command = "(turn 0)"
            if self.m_iTime == 1:
                command = "(turn 80)"
            elif self.m_iTime < 5:
                command = "(dash 100)"
            elif self.m_iTime == 5:
                command = "(turn 90)"
            elif self.m_iTime < 15:
                command = "(turn 0)(turn_neck -20)"
            elif self.m_iTime == 15:
                command = "(turn 30)(turn_neck 90)"
            elif self.m_iTime < 18:
                command = "(dash 100)"
            elif self.m_iTime == 18:
                command = "(kick 30 45)"

            self.m_strCommand[self.m_iTime] = command


if __name__ == "__main__":
    player16s = []
    for i in range(11):
        p16 = Player16()
        player16s.append(p16)
        teamname = "p16s"
        player16s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player16s[i].start()

    print("試合登録完了")