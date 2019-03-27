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
        req_msg = ''
        while True:
            data = connection.recv(32)
            req_msg = req_msg + data
            if (req_msg[-4:] == "\r\n\r\n"):
                break

        print req_msg
        baris = req_msg.split("\r\n")
        baris_request = baris[0]
        print baris_request
        a, url, c = baris_request.split(" ")

        if (url.startswith("/download")):
            respon = response_download(url)
        elif (url == '/') :
            respon = "HTTP/1.1 200 OK\r\n" \
            "Content-Type: text/plain\r\n" \
            "Content-Length: 19\r\n" \
            "\r\n" \
            "Connected to server"
        else:
            respon = "HTTP/1.1 200 OK\r\n" \
                     "Content-Type: text/plain\r\n" \
                     "Content-Length: 9\r\n" \
                     "\r\n" \
                     "Not found"

        connection.send(respon)

    finally:
        print "Closing socket"
        sock.close()

def response_download(req):
    url, name = req.split("=")
    print name
    file = open(name, 'rb').read()
    length = len(file)
    hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type:  multipart/form-data\r\n" \
            "Content-Length: {}\r\n" \
            "\r\n" \
            "{}".format(length, file)
    return hasil

while True:
    #wait a connection
    print>>sys.stderr, 'waiting for a connection...'
    #accepting connection
    connection, client_address = sock.accept()
    print>>sys.stderr, 'connection from', client_address
    #receive tha data in small chunks and retransmit it
    thread = Thread(target = handleRequest, args = (connection, client_address))
    thread.start()
