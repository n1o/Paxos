'''
Created on Dec 2, 2012

@author: marek
'''
import SocketServer
import mysql.connector

class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """

    def handle(self):
        print "Learned"
        listDatabaseItems()
        
def listDatabaseItems():
    conx = mysql.connector.connect(user='marek',database='PocitacoveSiete',password='pocitacovesiete')
    curA = conx.cursor(buffered=True)
    query = ("select * from User")
    curA.execute(query)
    for i in curA:
        print i
    conx.close()
    
if __name__ == "__main__":
    listDatabaseItems()
    
    
    HOST, PORT = "192.168.28.1", 9998
    #HOST, PORT = "192.168.28.128", 9998

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)
    

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()