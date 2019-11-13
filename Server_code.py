import socket
import threading
import os

def RetrFile(name, sock):
    filename = sock.recv(1024)
    if os.path.isfile(filename):
        sock.send("EXISTS " + str(os.path.getsize(filename)))
        userResponse = sock.recv(1024)
        if userResponse[:2] == 'OK':
            with open(filename, 'rb') as f:
                bytesToSend = f.read(1024)
                sock.send(bytesToSend)
                while bytesToSend != "":
                    bytesToSend = f.read(1024)
                    sock.send(bytesToSend)
    else:
        sock.send("ERR ")

    sock.close()

def Main():
    host = '192.168.43.21'
    port = 5000


    s = socket.socket()
    s.bind((host,port))

    s.listen(5)

    print("Server is ready to send the data")
    while True:
        c, addr = s.accept()
        print("client connedted ip:<" + str(addr) + ">")
        t = threading.Thread(target=RetrFile, args=("RetrThread", c))
        t.start()

    s.close()

if __name__ == '__main__':
    Main()
