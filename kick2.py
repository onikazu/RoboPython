from socket import *
import threading


class Playerex5(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.socket = socket(AF_INET, SOCK_DGRAM)
        self.HOSTNAME = "localhost"
        self.PORT = 6000
        self.ADDRESS = gethostbyname(self.HOSTNAME)
        self.m_strPlayMode = ""
        self.m_iNumber = 0
        self.m_strTeamName = ""
        self.m_strHostName = ""
        self.m_strSide = ""
        self.m_iNumber = 0
        self.m_dKickOffX = 0.0
        self.m_dKickOffY = 0.0

    def send(self, command):
        to_byte_command = command.encode(encoding='utf_8')
        self.socket.sendto(to_byte_command, (self.ADDRESS, self.PORT))
        # print("sending ", command, " is done")

    def receive(self):
        message, arr = self.socket.recvfrom(4096)
        message = message.decode("UTF-8")
        return message

    def initialize(self, number, team_name, server_name, server_port):
        self.m_iNumber = number
        self.m_strTeamName = team_name
        self.m_strHostName = server_name
        if self.m_iNumber == 1:
            command = "(init " + self.m_strTeamName + "(goalie))"
        else:
            command = "(init " + self.m_strTeamName + ")"
        self.send(command)

    def checkInitialMode(self):
        if self.m_strPlayMode.startswith("before_kick_off") or \
            self.m_strPlayMode.startswith("goal_l") or \
            self.m_strPlayMode.startswith("goal_r"):
            return True
        else:
            return False

    def getObjectMessage(self, message, keyword):
        result = ""
        index0 = message.find(keyword)
        while -1 < index0:
            index1 = message.find(")", index0+2)
            index2 = message.find(")", index1+1)
            result += message[index0:index2+1]
            result += ")"
            index0 = message.find(keyword, index2)
        return result

    def getPram(self, message, keyword, number):
        OUT_OF_RANGE = 999
        str = "(" + keyword
        index0 = message.find(str)
        if index0 < 0:
            return OUT_OF_RANGE

        index1 = message.find(" ", index0 + str.length())
        if number == 4:
            index1 = message.find(" ", index1 + 1)
        elif number == 3:
            index1 = message.find(" ", index1 + 1)
        elif number == 2:
            index1 = message.find(" ", index1 + 1)
        else:
            pass
        index2 = message.find(" ", index1+1)
        index3 = message.find(")", index1+1)
        if index3 < index2 and index3 != -1 or index2 == -1:
            index2 = index3
        result = 0.0
        try:
            result = float(message[index1:index2])
        except Exception:
            print("文字データによるエラー")
            result = OUT_OF_RANGE
        return result

    def run(self):
        while True:
            message = self.receive()
            # print(message)
            self.analyzeMessage(message)

    def analyzeInitialMessage(self, message):
        index0 = message.index(" ")
        index1 = message.index(" ", index0 + 1)
        index2 = message.index(" ", index1 + 1)
        index3 = message.index(")", index2 + 1)

        self.m_strSide = message[index0+1:index1]
        self.m_iNumber = int(message[index1+1:index2])
        self.m_strPlayMode = message[index2+1:index3]

    def analyzeVisualMessage(self):
        pass

    def analyzeAuralMessage(self, message):
        index0 = message.index(" ")
        index1 = message.index(" ", index0+1)
        index2 = message.index(" ", index1+1)
        index3 = message.index(")", index2+1)
        strSpeaker = message[index1+1:index2]
        strContent = message[index2+1:index3]

        if strSpeaker.startswith("referee"):
            self.m_strPlayMode = strContent

    def analyzeMessage(self, message):
        if isinstance(message, type(None)):
            pass
            # print(message)
        elif message.startswith("(init"):
            self.analyzeInitialMessage(message)
        elif message.startswith("(see "):
            self.analyzeVisualMessage()
            self.play(message)
        else:
            pass
            # print(message)

        if message.startswith("(hear "):
            self.analyzeAuralMessage(message)

    def kick(self, message):
        target_goal = ""
        if self.m_strSide.startswith("r"):
            target_goal = "(g l)"
        else:
            target_goal = "(g r)"
        index0 = message.find(target_goal)
        if index0 > -1:
            goalDist = self.getPram(message, target_goal, 1)
            goalDir = self.getPram(message, target_goal, 2)
            return "(kick 100 " + goalDir + ")"
        else:
            return "(kick 20 135)"


    def play(self, message, ballDist=None, ballDir=None):
        # ボールが見えていないときのplay
        if ballDist is None and ballDir is None:
            if self.checkInitialMode():
                self.setKickOffPosition()
                command = "(move " + str(self.m_dKickOffX) + " " \
                    + str(self.m_dKickOffY) + ")"
                self.send(command)
            else:
                message = message.replace("B", "b")
                ball = self.getObjectMessage(message, "((b")
                if ball.startswith("((b"):
                    ballDist = self.getPram(ball, "(b)", 1)
                    ballDir = self.getPram(ball, "(b)", 2)
                    self.play(message, ballDist, ballDir)
                else:
                    command = "(turn 30)"
                    self.send(command)
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
            # 体の正面にはない
            else:
                command = "(turn " + str(ballDir) + ")"
                print("c", command)
            self.send(command)

    def checkNearest(self, message, ballDist, ballDir):
        return True

    def setKickOffPosition(self):
        if self.m_iNumber == 1:
            self.m_dKickOffX = -50.0
            self.m_dKickOffY = -0.0
        elif self.m_iNumber == 2:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = -15.0
        elif self.m_iNumber == 3:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = -5.0
        elif self.m_iNumber == 4:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = +5.0
        elif self.m_iNumber == 5:
            self.m_dKickOffX = -40.0
            self.m_dKickOffY = +15.0
        elif self.m_iNumber == 6:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = -15.0
        elif self.m_iNumber == 7:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = -5.0
        elif self.m_iNumber == 8:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = +5.0
        elif self.m_iNumber == 9:
            self.m_dKickOffX = -20.0
            self.m_dKickOffY = +15.0
        elif self.m_iNumber == 10:
            self.m_dKickOffX = -1.0
            self.m_dKickOffY = -5.0
        elif self.m_iNumber == 11:
            self.m_dKickOffX = -4.0
            self.m_dKickOffY = +10.0
        else:
            print("範囲外の背番号の選手です")


if __name__ == "__main__":
    players = []
    for i in range(22):
        p = Playerex5()
        players.append(p)
        if i < 11:
            teamname = "left"
        else:
            teamname = "right"
        players[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        players[i].start()
    print("試合登録完了")
