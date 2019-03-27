import sys
import socket
import os
from threading import Thread
import glob

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_address = ('localhost', 10000)
print >> sys.stderr, 'starting up on %s port %s' %server_address
sock.bind(server_address)

sock.listen(1)

def loadImage():
    image = []
    image.extend(glob.glob('*.jpg'))
    image.extend(glob.glob('*.png'))
    return image

def handleReq(conn):
    files = loadImage()
    while True:
        data = conn.recv(32)
        if(data == 'fetch'):
            for i in files:
                conn.send(i + "\n")

while True:
    print "waiting for a connection"
    connection, client_address = sock.accept()
    print >> sys.stderr, 'connection from', client_address
    thread = Thread(target=handleReq, args=(connection, ))
    thread.start()
