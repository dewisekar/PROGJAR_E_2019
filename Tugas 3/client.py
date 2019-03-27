import sys
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

def requestList():
    msg = "fetch"
    sock.sendall(msg)
    msg = sock.recv(1024)        
    print msg

def requestBreak():
    msg ="break"
    sock.sendall(msg)

try:
    print "Cara menggunakan:\n1. Download = 'download/namafile' atau 'download/direktori/namafile"
    print "2. Upload = 'upload/namafile'"
    print "3. Melihat daftar file = 'fetch/direktori' atau 'fetch'"
    print "4. Exit: break"
    while True:
        #splitting command
        req = raw_input("Masukkan perintah: ")
        reqs = req.split("/")

        if(reqs[0]=="download"):
            ya=0
        elif(reqs[0]=="upload"):
            ya=1
        elif(reqs[0]=="fetch"):
            requestList()
        else:
            requestBreak()
            break

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()