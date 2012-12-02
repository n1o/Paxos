import socket
from threading import Timer
import time
from Queue import Queue


class ProposerServer(object):
    
    def __init__(self):
        self.HOSTS = list()
        self.NOTIFI = "NOTIFI"
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
    def send(self,message,host,port):
        try:
            # Create a socket (SOCK_STREAM means a TCP socket)
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(10)
            # Connect to server and send data
            sock.connect((host, port))
            sock.sendall(message)
            # Receive data from the server and shut down
            return sock.recv(1024)
        finally:
            sock.close()
            
    def sendAll(self,message):
        responses = list()
        for host in self.HOSTS:
            response = self.send(message, host,self.PORT)
            responses.append(response)
        return responses
    
    def notifiLearners(self):
        for host in self.HOSTS:
            self.send(self.NOTIFI, host, 9998)
            print "send learners"
        
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
while True:
    l = list()
    type = ""
    while(type!='u' and type!='i' and type!='d' and type!='q'):
        input = raw_input("Enter operation type: i for insert, d for delete, u for update, q for quit:")
        type = str(input)
    if(type=="u"):
        l.append(proposer.UPDATE)
    elif(type=="i"):
        l.append(proposer.INSERT)
        print proposer.INSERT
    elif(type=="d"):
        l.append(proposer.DROP)
    elif(type=="q"):
        break
    else:
        print type +" invalid choice"
        
    rodneCislo = ""
    
    while not len(rodneCislo)==11:
        print rodneCislo
        input = raw_input("Enter Personal NO: (11 signs) ")
        rodneCislo = str(input)
        print len(rodneCislo)
    
    l.append(rodneCislo)
    name = ""
    while len(name) == 0 or len(name)>20:
        input = raw_input("Enter First Name: (up to 20 signs) ")
        name = str(input)
        
    l.append(name)
    lastName=""
    while len(lastName) == 0 or len(lastName)>20:
        input = raw_input("Last Name: (up to 20 signs) ")
        lastName = str(input)
    l.append(lastName)
    
    while True:
        age = 0
        input = raw_input("Enter age: ")
        try:
            age = int(input)
            l.append(str(age))
            break
        except Exception:
            print input +" is not a number"

    data = proposer.createProposeMessage(l);
    responses = proposer.sendAll(data)
    if proposer.allPrommises(responses):
        message = proposer.createAcceptMessage(l)
        proposer.sendAll(message)
        print "Succes"
        proposer.notifiLearners()
        
    
    

    
    

