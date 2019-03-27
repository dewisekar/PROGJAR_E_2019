from threading import Thread
import sys
import socket

#create a tcp/ip socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#bind the socket to the port
server_address = ('localhost', 10000)
print>>sys.stderr,'Starting up on %s port %s' % server_address
sock.bind(server_address)

#listen for incoming connection
sock.listen(1)

#function for handle requests
def handleRequest(connection, client_address):
    try:
        print>>sys.stderr, 'Connection from', client_address

    finally:
        print "Closing socket"
        sock.close()

while True:
    #wait a connection
    print>>sys.stderr, 'waiting for a connection...'
    #accepting connection
    connection, client_address = sock.accept()
    print>>sys.stderr, 'connection from', client_address
    #receive tha data in small chunks and retransmit it
    thread = Thread(target = handleRequest, args = (connection, client_address))
    thread.start()
