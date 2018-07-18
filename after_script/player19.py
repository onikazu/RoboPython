import player18
import threading
from socket import *
import math


class Player19(player18.Player18, threading.Thread):
    def __init__(self):
        super(Player19, self).__init__()
        self.m_iBallTime = -6
        self.m_iSearchCount = 0

    def analyzeVisualMessage(self, message):
        super().analyzeVisualMessage(message)
        if message.find("(ball)") > -1:
            self.m_iBallTime = self.m_iVisualTime
            self.m_iSearchCount = 0
        elif self.checkFresh(self.m_iBallTime) == False:
            if self.m_iSearchCount == 0 and self.checkInitialMode() == False:
                self.m_iSearchCount = 9

    def checkFresh(self, time):
        if self.m_iTime - time > 3:
            return False
        else:
            return True

    def searchBall(self, searchCount):
        t = self.m_iTime
        if self.m_iSearchCount == 9:
            self.m_strCommand[t] += "(turn_neck 180)"
            self.m_strCommand[t] += "(change_view wide high)"
        if self.m_iSearchCount == 6:
            self.m_strCommand[t] += "(turn_neck -180)"
            self.m_strCommand[t] += "(change_view wide high)"
        if self.m_iSearchCount == 3:
            self.m_strCommand[t] = "(turn 180)"
            self.m_strCommand[t] += "(turn_neck 90)"
            self.m_strCommand[t] += "(change_view wide high)"

    def lookAt(self, faceX, faceY):
        t = self.m_iTime
        turn_angle = 0.0
        command = self.m_strCommand[t]
        if command.startswith("(turn")
            moment = self.getParam(command, "turn", 1)
            vx = self.m_dVX[t]
            vy = self.m_dVY[t]
            speed = math.sqrt(vx * vx + vy * vy)
            turn_angle = moment / (1 + self.inertia_moment * speed)

