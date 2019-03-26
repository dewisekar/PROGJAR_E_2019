import socket


#port
TARGET_IP = "127.0.0.1"
TARGET_PORT = 9000

#socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#sending signals to the server if the client is ready
sock.sendto("READY", (TARGET_IP, TARGET_PORT))
counter = 1

def receiveImage():
    while True:
        data, addr = sock.recvfrom(1024)
        if(data[0:5]=="START"):
            print "Menerima ",data[6:]
            fp = open(data[6:],'wb+')
            ditulis = 0
        elif(data=="DONE"):
            fp.close()
        elif(data=="END"):
            break
        else:
            print "Blok ", len(data), data[0:10]
            fp.write(data)      
       
while (counter == 1):
    data, addr = sock.recvfrom(1024)
    if(data=="SENDING"):
        receiveImage()
        counter = 0
    
    
    



       
    
             


