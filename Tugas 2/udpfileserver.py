from threading import Thread
import socket
import os

#setting IP and port
TARGET_IP = '127.0.0.1'
TARGET_PORT = 9000

#setting socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((TARGET_IP, TARGET_PORT))

#setting nama file gambar
namafile = ["bart.png", "bart2.png", "bart3.png", "bart4.png", "bart5.png"]

#fungsi buat ngirim gambar
def sendImage(trg_ip, trg_port):
    sock.sendto("SENDING", (trg_ip, trg_port))
    for i in namafile:
        #beritahu nama file yang dikirim
        sock.sendto("GAMBAR {}".format(i), (trg_ip, trg_port))
        ukuran = os.stat(i).st_size
        fp = open(i,'rb')
        k = fp.read()
        terkirim=0
        for x in k:
            sock.sendto(x, (trg_ip, trg_port))
            terkirim = terkirim + 1
            print "\r Terkirim {} of {} " . format(terkirim,ukuran)
        sock.sendto("DONE", (trg_ip, trg_port))
        fp.close()
    sock.sendto("END", (trg_ip, trg_port))

while True:
    print "Menunggu koneksi dari client..."
    data, addr = sock.recvfrom(1024)
    #signal from client
    if (data=="READY"):
        thread = Thread(target = sendImage, args = (TARGET_IP, TARGET_PORT))
        thread.start()

