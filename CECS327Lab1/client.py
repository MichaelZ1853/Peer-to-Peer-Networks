#CECS Lab Assignment 1
#Michael Zaragoza
#This is the client side of the program
import socket
import os
import pathlib

#Creates socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Creates the port for communication
port = 32701

#Grabs client's IP address
hostname = socket.gethostname()
ipAddress = socket.gethostbyname(hostname)

#Server's IP address
serverIPAddress = "192.168.1.145"

#Connects to the server
s.connect((serverIPAddress, port))

#Receives data from the server
while True:
    print(s.recv(1024).decode(encoding="utf-8"))

    #Makes a directory if computer is new to network
    directory = "Peer2PeerFolderClient"
    parentDirectory = pathlib.Path.home() / 'Desktop'
    mode = 0o666

    #Creates path directory
    path = os.path.join(parentDirectory, directory)
    try:
        os.mkdir(path, mode)
        print("Client folder created.")
    except FileExistsError:
        print("Directory already exists for this client.")
    except FileNotFoundError:
        print("Directory is not found on this client.")
    finally:
        clientData = str(ipAddress) + " " + str(path)
        s.send(clientData.encode(encoding="utf-8"))
        print(s.recv(1024).decode(encoding="utf-8"))

    #Keeps the client connected until server or client closes connection
    leaveSignal = ''
    while leaveSignal != "Bye":
        leaveSignal = s.recv(1024).decode(encoding="utf-8")
        print(leaveSignal)
    break
#Closes the connection
s.close()