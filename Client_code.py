import socket				# import socket for server client communication
import re

def main():
    host = '192.168.43.21'			# defines the IP address of the pi on which the server is set up
    port = 5000						# defines port that is used for communication

    s = socket.socket()				# open socket for communication
    s.connect((host, port))

    filename = "peoplestatus.txt"		# defines file that is to be received
    if filename != 'q':				# requests server to check for the given filename
        s.sendall(filename)
        data = s.recv(1024)
        if data[:6] == 'EXISTS':
            filesize = long(data[6:])		# creates a long type variable to store the incoming file
            message = "y"
            if message == 'y':
                s.send("OK")
                f = open('new_'+filename, 'wb')	#store the new file with the preceeding word 'new_'. w stands for write parameter.
                data = s.recv(1024)
                totalRecv = len(data)
                f.write(data)

                while totalRecv < filesize:
                    data = s.recv(1024)
                    totalRecv += len(data)
                    f.write(data)				# write the data to the new file
                    print("{0:.2f}".format((totalRecv/float(filesize))*100)+ "% Done")		# print the status of the file received

                print("Data is received to see")

                f.close()
		#print(data)

    s.close()		# close socket


if __name__ == '__main__':
    main()
