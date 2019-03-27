import sys
import socket

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 10000)
print >>sys.stderr, 'connecting to %s port %s' % server_address
sock.connect(server_address)

def requestBreak():
    msg ="break"
    sock.sendall(msg)

try:
    print "Cara menggunakan:\n1. Download = 'download/namafile'"
    print "2. Upload = 'upload/namafile'"
    print "3. Melihat daftar file = 'fetch'"
    print "4. Exit: break"
    while True:
        #splitting command
        req = raw_input("Masukkan perintah: ")
        reqs = req.split("/")
        sock.sendall(reqs[0])

        if(reqs[0]=="download"):
            sock.sendall(reqs[1])
            counter = sock.recv(32)
            if(counter == '1'):
                data = sock.recv(32)
                if(data[0:5]=="START"):
                    print "Menerima ",data[6:]
                    fp = open('cong.png','wb+')
                    ditulis = 0
                elif(data=="DONE"):
                    fp.close()
                else:
                    print "Blok ", len(data), data[0:10]
                    fp.write(data)

        elif(reqs[0]=="upload"):
            print "lel"
        elif(reqs[0]=="fetch"):
            msg = sock.recv(1024)        
            print msg
        else:
            requestBreak()
            break

finally:
    print >> sys.stderr, 'closing socket'
    sock.close()