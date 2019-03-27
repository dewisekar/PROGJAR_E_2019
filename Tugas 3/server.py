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
    #buat yang setara
    image = []
    image.extend(glob.glob('*.*'))
    return image
    for i in image:
        print i

def handleReq(conn):
    files = loadImage()
    for i in files:
        print(i)
    while True:
        data = conn.recv(32)
        if(data == 'fetch'):
            for i in files:
                conn.send(i + "\n")
        elif(data == 'download'):
            nama = conn.recv(32)
            print nama
            counter = '0'
            for i in files:
                if(nama == i):
                    counter = '1'
            print counter
            conn.send(counter)
            if(counter == '1'):
                conn.send("START {}" . format(nama))
                ukuran = os.stat(nama).st_size
                fp = open(nama,'rb')
                k = fp.read()
                terkirim=0
                for x in k:
                    conn.send(x)
                    terkirim = terkirim + 1
                    print "\r Terkirim {} of {} " . format(terkirim,ukuran)
                conn.send("DONE")
                fp.close()
        elif (data== 'upload'):
            while True:
                tron = conn.recv(32)
                if(tron[0:5]=="START"):
                    print "Menerima ",tron[6:]
                    fg = open('big.png','wb+')
                    ditulis = 0
                elif(tron=="DONE"):
                    print tron[0:6]
                    fg.close()
                    break
                else:
                    print "Blok ", len(tron), tron[0:10]
                    fg.write(tron)

while True:
    print "waiting for a connection"
    connection, client_address = sock.accept()
    print >> sys.stderr, 'connection from', client_address
    thread = Thread(target=handleReq, args=(connection, ))
    thread.start()
