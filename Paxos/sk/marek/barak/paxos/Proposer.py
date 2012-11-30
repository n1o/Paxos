import socket
import sys

HOST, PORT = "localhost", 9999
hosts = list()
hosts.append("localhost")
hosts.append("192.168.28.128")
data = " ".join(sys.argv[1:])

# Create a socket (SOCK_STREAM means a TCP socket)


for h in hosts:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # Connect to server and send data
        sock.connect((h, PORT))
        sock.sendall("DATA")

        # Receive data from the server and shut down
        received = sock.recv(1024)
    finally:
        sock.close()

    print "Sent:     {}".format(data)
    print "Received: {}".format(received)