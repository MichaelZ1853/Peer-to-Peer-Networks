#CECS Lab Assignment 1
#Michael Zaragoza
#This is the server side of the program/server also acts as a client

import socket
import ipaddress
import os
import pathlib
from time import sleep
from Node import Node

#Reads the file from a directory and return the file data
def readFile(directoryPath, file):
    with open(os.path.join(directoryPath, file), "rb") as fileContent:
        data = fileContent.read()
        fileContent.close()
        return data

#Creates a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Socket successfully created")

#Creates the port for communication
port = 32701

#grabs server's IP address
hostname = socket.gethostname()
sIpAddress = socket.gethostbyname(hostname)
sIpAddressOctets = str(sIpAddress).split('.')
sIpAddressFirstThree = sIpAddressOctets[0] + "." + sIpAddressOctets[1] + "." + sIpAddressOctets[2]

#Binds IP address and port to the socket
s.bind((sIpAddress, port))
print("Socket is binded to port %s" % (port))

#Puts the socket into listening mode
s.listen(3)
print("Socket is now listening for clients.")

#Creates a node list for the network
nodeNetwork = {}

#Makes a directory if computer is new to the local network
directory = "Peer2PeerFolderServer"
parentDirectory = pathlib.Path.home() / 'Desktop'
mode = 0o666

path = os.path.join(parentDirectory, directory)

#Creates path directory
try:
    os.mkdir(path, mode)
    print("Server folder created.")
except FileExistsError:
    print("Directory already exists for this server.")
except FileNotFoundError:
    print("Directory is not found on this server.")

#Creates server node
serverNode = Node(sIpAddress, path)
nodeNetwork.update({serverNode: os.listdir(serverNode.directoryPath)})

#Establishes connection with client.
c, address = s.accept()

#While loop to sustain connection
while True:
    sIpAddress = ipaddress.IPv4Network(sIpAddress)
    #Connects any client to the server
    print('Got connection from', address)

    #checks other IP addresses to determine if they are on the same network
    #Make sure to block 0 and 1 as last octets
    cIpAddress = ipaddress.IPv4Network(address[0])
    cIpAddressOctets = str(cIpAddress.network_address).split('.')
    cIpAddressFirstThree = cIpAddressOctets[0] + "." + cIpAddressOctets[1] + "." + cIpAddressOctets[2]

    if (cIpAddressFirstThree == sIpAddressFirstThree and str(cIpAddress.netmask) == str(sIpAddress.netmask)
    and cIpAddressOctets[3] != '0' and cIpAddressOctets[3] != '1'):
        #Sends a thank you message to the client
        c.send(str("Thank you for connecting to the server.").encode(encoding="utf-8"))

        #Creates client node
        clientData = c.recv(1024).decode(encoding="utf-8")
        clientDataArray = clientData.split(" ")
        clientNode = Node(clientDataArray[0], clientDataArray[1])
        nodeNetwork.update({clientNode: os.listdir(clientNode.directoryPath)})
        c.send(str("Thank you for sending client data.").encode(encoding="utf-8"))

        #Adds all files to the server's local dictionary/table to monitor all changes in the network
        allFiles = {}

        #Another while loop for synchronization
        while True:
            try:
                #Checks if all files are in sync with the files stored in the allFiles dictionary
                for node in nodeNetwork:
                    nodeFiles = node.getFiles()

                    #Checks for any changes to the nodes' files
                    if len(allFiles) != len(nodeFiles):
                        wasDeleted = len(allFiles) > len(nodeFiles)
                        wasAdded = len(allFiles) < len(nodeFiles)

                        #Takes different actions depending on what was changed
                        fileName = ""
                        if wasDeleted:
                            for file in allFiles:
                                #Removes file from server's local table
                                if (file not in nodeFiles):
                                    allFiles.pop(file)
                                    fileName = file
                                    break
                        if wasAdded:
                            for file in nodeFiles:
                                #Adds file to server's local table
                                if (file not in allFiles.keys()):
                                    data = readFile(node.directoryPath, file)
                                    allFiles[file] = data
                                    fileName = file
                                    break
                        print("Found changes in one of the nodes. Now syncing...")
                        #Updates all other nodes in the network
                        for otherNode in nodeNetwork:
                            otherNode.updateNode(allFiles, fileName, wasAdded, wasDeleted)
                        print("Synchronization complete.")
                sleep(1)
            except KeyboardInterrupt:
                #Ends client connection when client interrupts process with a key press
                c.send(str("Bye").encode(encoding="utf-8"))
                break
        break

#Closes the connection with the client
c.close()