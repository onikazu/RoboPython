import face_ball
import threading
from socket import *


class Player5(face_ball.Player4, threading.Thread):
    def __init__(self):
        super(Player5, self).__init__()

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
            if abs(ballDir) < 20.0:
                if ballDist < 1.0:
                    command = self.kick(message)
                elif self.checkNearest(message, ballDist, ballDir):
                    command = "(dash 80)"

            else:
                command = "(turn " + str(ballDir) + ")"
            self.send(command)

    def checkNearest(self, message, ballDist, ballDir):
        return True


if __name__ == "__main__":
    players = []
    for i in range(22):
        p = Player5()
        players.append(p)
        if i < 11:
            teamname = "left"
        else:
            teamname = "right"
        players[i].initialize((i % 11 + 1), teamname, "localhost", 6000)
        players[i].start()
    print("試合登録完了")
