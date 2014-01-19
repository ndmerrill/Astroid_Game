"""Server class"""
import socket
from Conversion import *

class Server():
    """Runs the Server"""
    def __init__(self, PORT):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setblocking(False)
        ip = self.getip()
        self.s.bind((ip, PORT))
        self.s.listen(1)
        print "Listening on ip " + ip

        self.users = {}

    ############################# RECIEVE ##################################
    def recieve(self):
        """Recieves connections from new users and data from others"""
        self.getNewConnections()
        allData = []
        for user in self.users:
            data = self.getData(user)
            if (data != ""):
                self.send(data, user)
                data = parse(data)
                allData.append(data[0])
        return allData

    def getNewConnections(self):
        """Checks for new users and connects with them"""
        try:
            conn, addr = self.s.accept()
            newName = conn.recv(10)
            for user in self.users:
                if (newName == user):
                    conn.sendall("N")
                    conn.close()
                    conn = "Er"
            if (conn != "Er"):
                conn.sendall("Y")
                
                conn.setblocking(False)

                self.users[newName] = conn
        except socket.error:
            pass

    def getData(self, user):
        """Recieves data from current users"""
        try:
            data = self.users[user].recv(2048)
        except socket.error:
            data = ""
        return data

    ########################### SEND #######################################
    def send(self, data, no=None):
        """Sends data to all users"""
        try:
            for user in self.users:
                if (user == no):
                    continue
                self.users[user].sendall(data)
        except socket.error:
            pass

    def sendMissile(self, x, y, b, r):
        t = encode([{"type":"S", "x":x, "y":y, "burning":b, "rotation":r}])
        self.send(t)

    def sendLocation(self, n, x, y, b, r):
        t=encode([{"type":"L","name":n,"x":x,"y":y,"burning":b,"rotation":r}])
        self.send(t)

    def sendExplode(self, x, y):
        t = encode([{"type":"E", "x":x, "y":y}])
        self.send(t)

    def sendRemove(self, n):
        t = encode([{"type":"R", "name":n}])
        self.send(t)

    def close(self):
        """Closes all connection"""
        for user in self.users:
            self.users[user].close()
        self.s.close()

    ########################### GETIP ######################################
    def getip(self):
        test = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        test.connect(("google.com", 80))
        host = test.getsockname()[0]
        return host
