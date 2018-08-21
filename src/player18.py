import player17
import threading
from socket import *
import math


class Player18(player17.Player17, threading.Thread):
    def __init__(self):
        super(Player18, self).__init__()
        self.m_iBallTime = 0
        self.m_debugLv18 = False

    def analyzeVisualMessage(self, message):
        # print("p18", message)
        super().analyzeVisualMessage(message)
        t = self.m_iVisualTime
        self.m_dX[t] = self.OUT_OF_RANGE
        self.m_dY[t] = self.OUT_OF_RANGE
        message = self.getLandMarker(message, self.m_dX[t], self.m_dY[t])
        self.m_dNeck[t] = self.getNeckDir(message)
        if self.m_dNeck[t] == self.OUT_OF_RANGE:
            return
        self.m_dBody[t] = self.normalizeAngle(self.m_dNeck[t] - self.m_dHeadAngle[t])
        pos = self.estimatePosition(message, self.m_dNeck[t], self.m_dX[t], self.m_dY[t])
        # ok
        if self.m_debugLv18:
            print("message: {}".format(message))
            print("p18 pos {}".format(pos))
            print("p18 ball: {} {}".format(self.m_dBallX[t], self.m_dBallY[t]))
        if pos["x"] == self.OUT_OF_RANGE:
            return
        if pos["y"] == self.OUT_OF_RANGE:
            return
        self.m_dX[t] = pos["x"]
        self.m_dY[t] = pos["y"]
        if message.find("(b)") == -1:
            return
        self.m_iBallTime = t
        ball = self.getObjectMessage(message, "((b")
        # string tokenizer の代わり
        st = ball.split(" ")
        # print("p18 st: {}".format(st))
        ball_dist = self.getParam(message, "(b)", 1)
        ball_dir = self.getParam(message, "(b)", 2)
        # 自己流=============意味無
        # if ball_dir == self.OUT_OF_RANGE:
        #     return
        # # ==================
        rad = math.radians(self.normalizeAngle(self.m_dNeck[t] + ball_dir))
        self.m_dBallX[t] = self.m_dX[t] + ball_dist * math.cos(rad)
        self.m_dBallY[t] = self.m_dY[t] + ball_dist * math.sin(rad)
        if self.m_iNumber==10:
            print("p18 ballX Y rad:", self.m_dBallX[t], self.m_dBallY[t], rad)
        self.m_dBallVX[t] = self.m_dBallVY[t] = 0
        if self.m_debugLv18:
            print("p18 rad: {}".format(rad))
            print("p18 ball: {} {}".format(self.m_dBallX[t], self.m_dBallY[t]))
            print("message: {}".format(message))
        if t > 0:
            pre = (t - 1) % self.GAME_LENGTH
            # print("mdballvy", type(self.m_dBallVY))
            # print("mdy", type(self.m_dY))
            self.m_dBallVX[t] = self.m_dX[t] - self.m_dX[pre]
            self.m_dBallVY[t] = self.m_dY[t] - self.m_dY[pre]

        ballR = 0.0
        ballRad = 0.0

        if len(st) > 4:
            dist_change = self.getParam(message, "(b)", 3)
            dir_change = self.getParam(message, "(b)", 4)
            vx = dist_change
            vy = dir_change * ball_dist * (math.pi / 180)
            ballR = math.sqrt(vx * vx + vy * vy)
            ballDeg = math.degrees(math.atan2(vy, vx))
            ballDegAbs = self.normalizeAngle(ball_dir + ballDeg + self.m_dNeck[t])
            ballRad = math.radians(ballDegAbs)
            vx_r = ballR * math.cos(ballRad)
            vy_r = ballR * math.sin(ballRad)
            self.m_dBallVX[t] = vx_r + self.m_dVX[t]
            # print(type(self.m_dBallVY), type(vy_r), type(self.m_dVY))
            self.m_dBallVY[t] = vy_r + self.m_dVY[t]

            a = self.m_dBallX[t]
            b = self.m_dBallY[t]
            c = self.m_dBallVX[t]
            d = self.m_dBallVY[t]
            e = self.m_dX[t]
            f = self.m_dY[t]
            g = self.m_dVX[t]
            h = self.m_dVY[t]

            if self.m_debugLv18 and t < 30:
                print("時刻{0:.4f}, 位置{1:.4f}, {2:.4f}".format(self.m_iTime, self.m_dX[self.m_iTime], self.m_dY[self.m_iTime]))
                print("速度{0:.4f},{1:.4f}".format(self.m_dVX[self.m_iTime], self.m_dVY[self.m_iTime]))
                print("ball_dist{}".format(ball_dist))
                print("ball_dir{}".format(ball_dir))
                print("ボール位置{0:.4f}, {1:.4f}".format(self.m_dBallX[self.m_iTime], self.m_dBallY[self.m_iTime]))
                print("ボール速度{0:.4f}, {1:.4f}".format(self.m_dBallVX[self.m_iTime], self.m_dBallVY[self.m_iTime]))
                print("ball = {}".format(ball))
                print("ballR:", ballR)
                print("ballRad", ballRad)


if __name__ == "__main__":
    player18s = []
    for i in range(11):
        p18 = Player18()
        player18s.append(p18)
        teamname = "p18s"
        player18s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player18s[i].start()

    player18s[9].m_debugLv18 = True

    print("試合登録完了")
