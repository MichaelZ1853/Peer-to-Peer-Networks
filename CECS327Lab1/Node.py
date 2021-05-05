import os

class Node:
    #Constructor
    def __init__(self, ipAddress, directoryPath):
        self.ipAddress = ipAddress
        self.directoryPath = directoryPath

    #Updates the node with current files
    def updateNode(self, files, currentFile, wasAdded, wasDeleted):
        if wasAdded:
            self.addFile(files, currentFile)
        if wasDeleted:
            if (currentFile in os.listdir(self.directoryPath)):
                self.deleteFile(currentFile)

    #gets all the files in the directory
    def getFiles(self):
        return os.listdir(self.directoryPath)

    #adds the file to the node
    def addFile(self, files, file):
        print("Adding file..")
        fileName = os.path.join(self.directoryPath, file)
        newFile = open(fileName, "wb")
        newFile.write(files[file])
        newFile.close()

    #deletes the file from the node
    def deleteFile(self, file):
        print("Deleting file...")
        filePath = os.path.join(self.directoryPath, file)
        if os.path.isfile(filePath):
            os.remove(filePath)

    #Prints file names from the node
    def printFiles(self):
        filesList = os.listdir(self.directoryPath)
        print(filesList)