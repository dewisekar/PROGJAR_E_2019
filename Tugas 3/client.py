import sys
import socket
import glob
import os

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

def loadFile():
    image = []
    image.extend(glob.glob('*.*'))
    return image

try:
    print "Cara menggunakan:\n1. Download = 'download/namafile'"
    print "2. Upload = 'upload/namafile'"
    print "3. Melihat daftar file = 'fetch'"
    print "4. Exit: break"
    files = loadFile()
    while True:
        #splitting command
        req = raw_input("Masukkan perintah: ")
        reqs = req.split("/")
        sock.sendall(reqs[0])

        if(reqs[0]=="download"):
            sock.sendall(reqs[1])
            counter = sock.recv(32)
            if(counter == '1'):
                while True:
                    data = sock.recv(32)
                    if(data[0:5]=="START"):
                        print "Menerima ",data[6:]
                        fp = open(data[6:],'wb+')
                        ditulis = 0
                    elif(data=="DONE"):
                        print data[0:6]
                        fp.close()
                        break
                    else:
                        print "Blok ", len(data), data[0:10]
                        fp.write(data)
            else:
                print "File tidak ditemukan"

        elif(reqs[0]=="upload"):
            sock.send(reqs[1])
            sock.send("START {}" . format(reqs[1]))
            ukuran = os.stat(reqs[1]).st_size
            fp = open(reqs[1],'rb')
            k = fp.read()
            terkirim=0
            for x in k:
                sock.send(x)
                terkirim = terkirim + 1
                print "\r Terkirim {} of {} " . format(terkirim,ukuran)
            fp.close()
            sock.send("DONE")
            

        elif(reqs[0]=="fetch"):
            msg = sock.recv(1024)        
            print msg
        elif(reqs[0]=="break"):
            break

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()