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
        self.INSERT = "INSERT"
        self.UPDATE = "UPDATE"
        self.DROP = "DROP"
        self.PROMIS = "PROMIS"
        self.messageValue = 0
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
        return responses
            
    def getValue(self):
        val = int(round(time.time() * 100000))
        if self.LEADER:
            val += self.LEADER_BONUS
        return val
        
    def createMessage(self,baseMessage,messageList):
        for item in messageList:
            baseMessage+=item +";"
        return baseMessage
    
    def allPrommises(self,items):
        for item in items:
            if self.parseMessage(item).pop(1)!=self.PROMIS:
                return False
        return True
    def createProposeMessage(self,messageList):
        self.setLeader()
        self.messageValue = str(self.getValue())
        message =self.messageValue+";"
        message += self.PROPOSE+";"
        return self.createMessage(message, messageList)
    
    def getInterval(self):
        now = time.localtime()
        val =  60 - now.tm_sec
        return val
    def createAcceptMessage(self,messageList):
        baseMessage = str(self.messageValue) + ";"
        baseMessage += self.ACCEPT+";"
        return self.createMessage(baseMessage, messageList)
    
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
l.append(proposer.INSERT)
l.append("891001/7204")
l.append("Marek")
l.append("Barak")
l.append("23")

data = proposer.createProposeMessage(l);
responses = proposer.sendAll(data)
if proposer.allPrommises(responses):
    message = proposer.createAcceptMessage(l)
    proposer.sendAll(message)
    
    

    
    

