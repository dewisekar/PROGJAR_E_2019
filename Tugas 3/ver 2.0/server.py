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

def post_receiver():

    #m = open("metadata", "wb")
    req_msg = ''
    while True:
        data = koneksi_client.recv(64)
        req_msg = req_msg+data

        if (len(data) < 64):
            #m.write(req_msg)
            filename = req_msg.split('filename="')
            filename = filename[1]
            index = filename.find('"')
            filename = filename[:index:]
            f = open(filename, "wb")
            req_msg = req_msg.split("Content-Type: ")
            req_msg = req_msg[2]
            print req_msg[-60::]
            index = req_msg.find("\r\n\r\n")
            req_msg = req_msg[index+4::]
            req_msg = req_msg.split("\n\r\n------WebKitForm")
            break
    f.write(req_msg[0])
    f.close()


#function for handle requests
# fungsi melayani client
def handleRequest(koneksi_client, alamat_client):
    try:
        print >> sys.stderr, 'ada koneksi dari ', alamat_client
        req_msg = ''
        while True:
            data = koneksi_client.recv(64)
            #data = bytes.decode(data)
            req_msg = req_msg + data
            if req_msg.startswith("POST") :
                post_receiver()
                break
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

        koneksi_client.send(respon)
    finally:
        # Clean up the connection
        koneksi_client.close()

def response_download(req):
    url, filename = req.split('=')
    print filename
    file = open(filename, 'rb').read()
    panjang = len(file)
    hasil = "HTTP/1.1 200 OK\r\n" \
            "Content-Type:  multipart/form-data\r\n" \
            "Content-Length: {}\r\n" \
            "\r\n" \
            "{}".format(panjang, file)
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
