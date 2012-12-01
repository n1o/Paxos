import socket
from threading import Timer
import time
from Queue import Queue


class ProposerServer(object):
    
    def __init__(self):
        self.HOSTS = list()
        self.HOSTS.append("192.168.28.1")
        self.HOSTS.append("192.168.28.128")
        self.PORT = 9999
        self.messageQueue = Queue()
        self.PROPOSE = "PROPOSE"
        self.ACCEPT = "ACCEPT"
        self.LEADER_BONUS = 500000
        self.LEADER = False
        self.CREATE = "CREATE"
        self.UPDATE = "UPDATE"
        self.DROP = "DROP"
        self.PROMIS = "PROMIS"
    def send(self,message,host):
        try:
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            # Connect to server and send data
            sock.connect((host, self.PORT))
            sock.sendall(message)
            # Receive data from the server and shut down
            return sock.recv(1024)
        finally:
            sock.close()
            
    def sendAll(self,message):
        responses = list()
        for host in self.HOSTS:
            response = self.send(message, host)
            responses.append(response)
        
            
    def getValue(self,leader):
        val = int(round(time.time() * 100000))
        if leader:
            val += self.LEADER_BONUS
        return val
        
    def createMessage(self,messageType,messageList):
        self.setLeader()
        message = ""
        message +=str(self.getValue(self.LEADER))+ ";"
        message +=messageType + ";"
        for item in messageList:
            message+=item +";"
        return message
    def isPromis(self,items):
        for item in items:
            if self.parseMessage(item).pop(1)!=self.PROMIS:
                return False
        return True
    
    def getInterval(self):
        now = time.localtime()
        val =  60 - now.tm_sec
        return val
    
    def setLeader(self):
        val = self.getInterval()/10
        if val % 2 == 1:
            self.LEADER = True
            
    def parseMessage(self,data):
        val = data.split(";")
        elements = list()
        for item in val:
            if not item == "":
                elements.append(item)
        return elements
proposer = ProposerServer()
l = list()
l.append(proposer.CREATE)
l.append("THing")
l.append("JOP")

data = proposer.createMessage(proposer.PROPOSE,l)
proposer.sendAll(data)

    
    

