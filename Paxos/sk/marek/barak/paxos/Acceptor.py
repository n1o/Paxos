'''
Created on Nov 30, 2012

@author: marek
'''
import SocketServer
import mysql.connector

class MyTCPHandler(SocketServer.BaseRequestHandler):
    def __init__(self, request, client_address, server):
        print "INIT"
        self.PROPOSE = "PROPOSE"
        self.ACCEPT = "ACCEPT"
        self.PROMIS = "PROMIS"
        self.INSERT = "INSERT"
        self.UPDATE = "UPDATE"
        self.DROP = "DROP"
        self.lastAccepted = self.getLastAccepted()
        SocketServer.BaseRequestHandler.__init__(self, request, client_address, server)
        
    def handle(self):
        # self.request is the TCP socket connected to the client
        
        self.data = self.request.recv(1024).strip()
        elements = self.parseMessage(self.data)
        lastAccepted = int(elements.pop(0))
        messageType = elements.pop(0)
        if self.lastAccepted < lastAccepted and self.PROPOSE == messageType:
            print "handle propose"
            self.writeLastPrommised(lastAccepted)
            self.lastAccepted = lastAccepted
            self.data = str(self.lastAccepted)+";"+self.PROMIS
            for item in elements:
                self.data+=";"+item
        elif self.lastAccepted == lastAccepted and self.ACCEPT == messageType:
            print "handle accept"
            type = elements.pop(0)
            if type == self.INSERT:
                print "INSERT"
                self.insertIntoUsers(elements)
            elif type == self.UPDATE:
                print "UPDATE"
                self.updateUsers(elements)
            elif type==self.DROP:
                print "DELETE"
                self.deleteUser(elements)
            else:
                print "Wrong message"
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
            
    def writeLastPrommised(self,accepted):
        try:
            f = open("./conf","r+")
            f.write(str(accepted))
        except IOError:
            print "NOT FOUND"
            
    def insertIntoUsers(self,values):
        conx = mysql.connector.connect(user='marek',database='PocitacoveSiete',password='pocitacovesiete')
        curA = conx.cursor(buffered=True)
        query = ("insert into User(user_id,name,last_name,age)"
                 "values(%s,%s,%s,%s)")
        curA.execute(query,(values.pop(0),values.pop(0),values.pop(0),int(values.pop(0))))
        conx.commit()
        conx.close()
        
    def updateUsers(self,values):
        conx = mysql.connector.connect(user='marek',database='PocitacoveSiete',password='pocitacovesiete')
        curA = conx.cursor(buffered=True)
        query = ("update User set name = %s, last_name = %s,age=%s where user_id = %s")
        curA.execute(query,(values.pop(1),values.pop(1),int(values.pop(1)),values.pop(0)))
        conx.commit()
        conx.close()
        
    def deleteUser(self,values):
        conx = mysql.connector.connect(user='marek',database='PocitacoveSiete',password='pocitacovesiete')
        curA = conx.cursor(buffered=True)
        query = ("delete from User where user_id = '"+values.pop(0)+"'")
        curA.execute(query)
        conx.commit()
        conx.close()
            
if __name__ == "__main__":
    HOST, PORT = "192.168.28.1", 9999
    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()