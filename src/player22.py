import player21
import threading
from socket import *
import math


class Player22(player21.Player21, threading.Thread):
    def __init__(self):
        super(Player22, self).__init__()
        self.m_listPlayer = []
        self.m_debugLv22 = False

    def getObjectList(self, message, keyword):
        list = []
        index0 = message.find(keyword)
        while index0 > -1:
            index1 = message.find(")", index0 + 2)
            index2 = message.find(")", index1 + 1)
            strObject = message[index0:index2+1]
            player = self.getObjectMessage_1(strObject)
            list.append(player)
            index0.find(keyword, index2)
        return list

    def getObjectMessage_1(self, obj):
        t = self.m_iTime
        dist = 0
        dir = 0
        dist_change = 0
        dir_change = 0
        neck = 0
        body = 0
        index0 = obj.find(") ")
        index1 = obj.find(")", index0 + 1)
        result = ""
        name = obj[0:index0+2]
        index2 = name.find("\"")
        index3 = name.find("\"", index2 + 1)
        index4 = name.find(")")
        s = "((p \"" + self.m_strTeamName + "\""
        team = ""
        if name.startswith(s):
            team = "friend"
        else:
            team = "enemy"
        number = 0
        if index3 + 1 < index4 and name.find("(p)") == -1 and name.find("(P)"):
            str = name[index3+1:index4]
            if str.find("goalie") > 0:
                str = str.replace("goalie", " ", 1)
            number = int(float(str))
        str = obj[index0+1:index1]
