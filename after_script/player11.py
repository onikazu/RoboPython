# フィールドの状況予測を行う
import player10
import threading
from socket import *
import math


class Player11(player10.Player10, threading.Thread):
    def __init__(self):
        super(Player11, self).__init__()
        self.GAME_LENGTH = 6000
        self.m_strServerParam = ""
        self.m_strPlayerParam = ""
        self.m_strPlayerType = []
        self.m_iPlayerType = 0
        self.m_strCommand = []
        for _ in range(6000):
            self.m_strCommand.append(0)
        self.m_iTime = -1
        self.m_iVisualTime = -1

    def analyzeServerParam(self, message):
        self.m_strServerParam = message

    def analyzePlayerParam(self, message):
        self.m_strPlayerParam = message

    def analyzePlayerType(self, message):
        id = int(self.getParam(message, "see", 1))
        self.m_strPlayerType[id] = message

    def analyzePhysicalMessage(self, message):
        self.m_iTime = int(self.getParam(message, "sense_body", 1))

    def predictMoveCommand(self, i):
        pass

    def predictDashCommand(self, i):
        pass

    def predictTurnCommand(self, i):
        pass

    def predictKickCommand(self, i):
        pass

    def predict(self, start, end):
        if self.m_iVisualTime < 0:
            return
        for i in range(start, end):
            self.predictMoveCommand(i)
            self.predictDashCommand(i)
            self.predictTurnCommand(i)
            self.predictKickCommand(i)

        if self.m_iTime > 0 and self.m_iTime < 20:
            print()
            print("時刻　体調情報", self.m_iTime)
            print("視覚情報＝", self.m_iVisualTime)

    def play_0(self):
        self.m_strCommand[self.m_iTime] = "(turn 0)"
        # 教科書誤植？
        if self.checkInitialMode():
            self.setKickOffPosition()
            command = \
            "(move " + str(self.m_dKickOffX) + " " + str(self.m_dKickOffY) + ")"
            self.m_strCommand[self.m_iTime] = command

    def analyzeMessage(self, message):
        # 初期メッセージの処理
        if message.startswith("(init "):
            self.analyzeInitialMessage(message)
        # 視覚メッセージの処理
        elif message.startswith("(see "):
            self.analyzeVisualMessage(message)
        # 体調メッセージの処理
        elif message.startswith("(sense_body "):
            self.analyzePhysicalMessage(message)
            if self.m_iVisualTime < self.m_iTime:
                self.predict(self.m_iVisualTime, self.m_iTime)
            self.play_0()
            self.send(self.m_strCommand[self.m_iTime])
        # 聴覚メッセージの処理
        elif message.startswith("(hear "):
            self.analyzeAuralMessage(message)
        # サーバパラメータの処理
        elif message.startswith("(server_param "):
            self.analyzeServerParam(message)
        # プレーヤーパラメータの処理
        elif message.startswith("(player_param "):
            self.analyzePlayerParam(message)
        # プレーヤータイプの処理
        elif message.startswith("(player_type "):
            self.analyzePlayerType(message)
        # エラーの処理
        else:
            print("error from server")

if __name__ == "__main__":
    player11s = []
    for i in range(11):
        p11 = Player11()
        player11s.append(p11)
        teamname = "p11s"
        player11s[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        player11s[i].start()

    print("試合登録完了")