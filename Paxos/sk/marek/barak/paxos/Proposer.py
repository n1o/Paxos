import socket
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
        self.LEADER_BONUS = 3000000
        self.isLeader = False
        
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
        for host in self.HOSTS:
            message = self.send(message, host)
            print message
            
    def getValue(self,leader):
        import time
        val = int(round(time.time() * 100000))
        if leader:
            val += self.LEADER_BONUS
        return val
        
    def createMessage(self,messageType,messageList,leader):
        message = ""
        message +=str(self.getValue(leader))+ ";"
        message +=messageType + ";"
        for item in messageList:
            message+=item +";"
        return message
    
        
proposer = ProposerServer()
l = list()
l.append("THing")
l.append("JOP")

data = proposer.createMessage(proposer.PROPOSE,l, False)
proposer.sendAll(data)

