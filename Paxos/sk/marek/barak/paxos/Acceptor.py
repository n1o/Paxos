'''
Created on Nov 30, 2012

@author: marek
'''
import SocketServer

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        print "INIT"
        self.PROPOSE = "PROPOSE"
        self.ACCEPT = "ACCEPT"
        self.PROMIS = "PROMIS"
        self.lastAccepted = self.getLastAccepted()
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        
        
    def handle(self):
        # self.request is the TCP socket connected to the client
        
        self.data = self.request.recv(1024).strip()
        elements = self.parseMessage(self.data)
        lastAccepted = int(elements.pop(0))
        if self.lastAccepted < lastAccepted and self.PROPOSE == elements.pop(0):
            print "handle propose"
            self.writeLastAccepted(lastAccepted)
            self.lastAccepted = lastAccepted
            self.data = str(self.lastAccepted)+";"+self.PROMIS
            for item in elements:
                self.data+=";"+item
        elif self.lastAccepted < lastAccepted and self.ACCEPT == elements.pop(0):
            print "handle accept"
        else:
            print "hanlde reject:"
            
        print self.data
        # just send back the same data, but upper-cased
        self.request.sendall(self.data.upper())
    def parseMessage(self,data):
        val = data.split(";")
        elements = list()
        for item in val:
            if not item == "":
                elements.append(item)
        return elements
    
    def getLastAccepted(self):
        try:
            f = open("./conf","r+")
            line = f.readline();
            if line != "":
                return int(line)
            else: return 0
        except IOError:
            print "NOT FOUND"
            
    def writeLastAccepted(self,accepted):
        try:
            f = open("./conf","r+")
            f.write(str(accepted))
        except IOError:
            print "NOT FOUND"
            
if __name__ == "__main__":
    HOST, PORT = "192.168.28.1", 9999
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()