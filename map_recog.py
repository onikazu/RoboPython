import no_look_shoot
import threading
from socket import *
import math


class Player8(no_look_shoot.Player7, threading.Thread):
    def __init__(self):
        super(Player8, self).__init__()
        self.m_strFlagName = []
        self.m_dFlagX = []
        self.m_dFlagY = []
        self.m_dX = 0.0
        self.m_dY = 0.0
        self.m_dNeck = 0.0
        self.m_strFlagName.append("goal r");     self.m_dFlagX.append(52.5);self.m_dFlagY.append(0.0  )
        self.m_strFlagName.append("goal l");     self.m_dFlagX.append(-52.5);self.m_dFlagY.append(0.0  )
        self.m_strFlagName.append("flag c t");   self.m_dFlagX.append(0.0  );self.m_dFlagY.append(-34.0)
        self.m_strFlagName.append("flag c b");   self.m_dFlagX.append(0.0)  ;self.m_dFlagY.append(+34.0)
        self.m_strFlagName.append("flag c");     self.m_dFlagX.append(0.0	);self.m_dFlagY.append(0.0  )
        self.m_strFlagName.append("flag p l t"); self.m_dFlagX.append(-36.0);self.m_dFlagY.append(-20.16)
        self.m_strFlagName.append("flag p l b"); self.m_dFlagX.append(-36.0);self.m_dFlagY.append( 20.16)
        self.m_strFlagName.append("flag p l c"); self.m_dFlagX.append(-36.0);self.m_dFlagY.append( 0.0 )
        self.m_strFlagName.append("flag p r t"); self.m_dFlagX.append( 36.0);self.m_dFlagY.append(-20.16)
        self.m_strFlagName.append("flag p r b"); self.m_dFlagX.append( 36.0);self.m_dFlagY.append( 20.16)
        self.m_strFlagName.append("flag p r c"); self.m_dFlagX.append( 36.0);self.m_dFlagY.append(  0.0)
        self.m_strFlagName.append("flag g l t"); self.m_dFlagX.append(-52.5);self.m_dFlagY.append(-7.01)
        self.m_strFlagName.append("flag g l b"); self.m_dFlagX.append(-52.5);self.m_dFlagY.append( 7.01)
        self.m_strFlagName.append("flag g r t"); self.m_dFlagX.append( 52.5);self.m_dFlagY.append(-7.01)
        self.m_strFlagName.append("flag g r b"); self.m_dFlagX.append( 52.5);self.m_dFlagY.append( 7.01)
        self.m_strFlagName.append("flag t l 50");self.m_dFlagX.append(-50.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t l 40");self.m_dFlagX.append(-40.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t l 30");self.m_dFlagX.append(-30.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t l 20");self.m_dFlagX.append(-20.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t l 10");self.m_dFlagX.append(-10.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t 0");   self.m_dFlagX.append(  0.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t r 10");self.m_dFlagX.append( 10.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t r 20");self.m_dFlagX.append( 20.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t r 30");self.m_dFlagX.append( 30.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t r 40");self.m_dFlagX.append( 40.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag t r 50");self.m_dFlagX.append( 50.0);self.m_dFlagY.append(-39.0)
        self.m_strFlagName.append("flag b l 50");self.m_dFlagX.append(-50.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b l 40");self.m_dFlagX.append(-40.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b l 30");self.m_dFlagX.append(-30.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b l 20");self.m_dFlagX.append(-20.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b l 10");self.m_dFlagX.append(-10.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b 0");   self.m_dFlagX.append(  0.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b r 10");self.m_dFlagX.append( 10.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b r 20");self.m_dFlagX.append( 20.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b r 30");self.m_dFlagX.append( 30.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b r 40");self.m_dFlagX.append( 40.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag b r 50");self.m_dFlagX.append( 50.0);self.m_dFlagY.append( 39.0)
        self.m_strFlagName.append("flag l t 30");self.m_dFlagX.append(-57.5);self.m_dFlagY.append(-30.0)
        self.m_strFlagName.append("flag l t 20");self.m_dFlagX.append(-57.5);self.m_dFlagY.append(-20.0)
        self.m_strFlagName.append("flag l t 10");self.m_dFlagX.append(-57.5);self.m_dFlagY.append(-10.0)
        self.m_strFlagName.append("flag l 0");   self.m_dFlagX.append(-57.5);self.m_dFlagY.append(  0.0)
        self.m_strFlagName.append("flag l b 10");self.m_dFlagX.append(-57.5);self.m_dFlagY.append( 10.0)
        self.m_strFlagName.append("flag l b 20");self.m_dFlagX.append(-57.5);self.m_dFlagY.append( 20.0)
        self.m_strFlagName.append("flag l b 30");self.m_dFlagX.append(-57.5);self.m_dFlagY.append( 30.0)
        self.m_strFlagName.append("flag r t 30");self.m_dFlagX.append( 57.5);self.m_dFlagY.append(-30.0)
        self.m_strFlagName.append("flag r t 20");self.m_dFlagX.append( 57.5);self.m_dFlagY.append(-20.0)
        self.m_strFlagName.append("flag r t 10");self.m_dFlagX.append( 57.5);self.m_dFlagY.append(-10.0)
        self.m_strFlagName.append("flag r 0");   self.m_dFlagX.append( 57.5);self.m_dFlagY.append(  0.0)
        self.m_strFlagName.append("flag r b 10");self.m_dFlagX.append( 57.5);self.m_dFlagY.append( 10.0)
        self.m_strFlagName.append("flag r b 20");self.m_dFlagX.append( 57.5);self.m_dFlagY.append( 20.0)
        self.m_strFlagName.append("flag r b 30");self.m_dFlagX.append( 57.5);self.m_dFlagY.append( 30.0)
        self.m_strFlagName.append("flag l t");   self.m_dFlagX.append(-52.5);self.m_dFlagY.append(-34.0)
        self.m_strFlagName.append("flag l b");   self.m_dFlagX.append(-52.5);self.m_dFlagY.append( 34.0)
        self.m_strFlagName.append("flag r t");   self.m_dFlagX.append( 52.5);self.m_dFlagY.append(-34.0)
        self.m_strFlagName.append("flag r b");   self.m_dFlagX.append( 52.5);self.m_dFlagY.append( 34.0)

    def getDistance(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0
        return math.sqrt(dx * dx + dy * dy)

    # メッセージに大文字が含まれていないために、省略（バージョンの仕様？？）
    def getLandMarker(self, message, playerX, playerY):
        pass

    # 返り値は辞書型になっている。教科書と違うので注意
    def estimatePosition(self, message, neckDir, playerX, playerY):
        result = { "x" : 999, "y" : 999}
        flag = self.getObjectMessage(message, "((g") + \
            self.getObjectMessage(message, "((f")
        index0 = flag.find("((")
        X = Y = W = S = 0.0
        flags = 0
        while index0 > -1:
            index1 = flag.find(")", index0 + 2)
            index2 = flag.find(")", index1 + 1)
            name = flag[index0+2:index1]
            j = 0
            while self.m_strFlagName.endswith(name) is False:
                j += 1
            dist = self.getParam(flag, name, 1)
            dir = self.getParam(flag, name, 2)
            rad = math.radians(self.normalizeAngle(dir + neckDir))
            W += 1 / dist
            X += W * (self.m_dFlagX[j] - dist * math.cos(rad))
            Y += W * (self.m_dFlagY[j] - dist * math.sin(rad))
            S += W
            flags += 1
            index0 = flag.find("((", index0 + 2)

        if flags > 0:
            result["x"] = X / S
            result["y"] = Y / S
        return result

    # @override
    def analyzeVisualMessage(self, message):
        OUT_OF_RANGE = 999.0
        time = int(self.getParam(message, "see", 1))
        if time < 1:
            return
        self.m_dNeck = self.getNeckDir(message)
        if self.m_dNeck == OUT_OF_RANGE:
            return
        if self.checkInitialMode():
            self.m_dX = self.m_dKickOffX
            self.m_dY = self.m_dKickOffY

        pos = self.estimatePosition(message, self.m_dNeck, self.m_dX, self.m_dY)
        self.m_dX = pos["x"]
        self.m_dY = pos["y"]
        


if __name__ == "__main__":
    player8s = []
    for i in range(11):
        p8 = Player8()
        player8s.append(p8)
        teamname = "p8s"
        player8s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player8s[i].start()
    player7s = []
    for i in range(11):
        p7 = no_look_shoot.Player7()
        player7s.append(p7)
        teamname = "p7s"
        player7s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player7s[i].start()

    print("試合登録完了")
