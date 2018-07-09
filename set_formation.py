import set_players
import threading
from socket import *


class Player2(set_players.Player1, threading.Thread):
    def __init__(self):
        super(Player2, self).__init__()
        self.m_dKickOffX = 0.0
        self.m_dKickOffY = 0.0

    def checkInitialMode(self):
        if m_strPlayMode.startswith("before_kick_off") or \
            m_strPlayMode.startswith("goal_l") or \
            m_strPlayMode.startswith("goal_r"):
            return True
        else:
            return False

    def analyzeVisualMessage(self):
        pass

    def setKickOffPosition(self):
        if self.m_iNumber == 1:
            m_dKickOffX = -50.0
            m_dKickOffY = -0.0
        elif self.m_iNumber == 2:
            m_dKickOffX = -40.0
            m_dKickOffY = -15.0
        elif self.m_iNumber == 3:
            m_dKickOffX = -40.0
            m_dKickOffY = -5.0
        elif self.m_iNumber == 4:
            m_dKickOffX = -40.0
            m_dKickOffY = +5.0
        elif self.m_iNumber == 5:
            m_dKickOffX = -40.0
            m_dKickOffY = +15.0
        elif self.m_iNumber == 6:
            m_dKickOffX = -20.0
            m_dKickOffY = -15.0
        elif self.m_iNumber == 7:
            m_dKickOffX = -20.0
            m_dKickOffY = -5.0
        elif self.m_iNumber == 8:
            m_dKickOffX = -20.0
            m_dKickOffY = +5.0
        elif self.m_iNumber == 9:
            m_dKickOffX = -20.0
            m_dKickOffY = +15.0
        elif self.m_iNumber == 10:
            m_dKickOffX = -1.0
            m_dKickOffY = -5.0
        elif self.m_iNumber == 11:
            m_dKickOffX = -4.0
            m_dKickOffY = +10.0
        else:
            print("範囲外の背番号の選手です")

    def play(self, message):
        if checkInitialMode():
            setKickOffPosition()
            command = "(move " + m_dKickOffX + " " + m_dKickOffY + ")"
        send(command)

    def analyzeMessage(self, message):
        super().analyzeMessage(message)
        if message.startswith("(see "):
            analyzeVisualMessage()
            play(message)


if __name__ == "__main__":
    players = []
    for i in range(22):
        p = Player2()
        players.append(p)
        if i < 11:
            teamname = "left"
        else:
            teamname = "right"
        players[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        players[i].start()
    print("試合登録完了")
