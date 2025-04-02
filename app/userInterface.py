from colours import bcolors
from pathlib import Path
import socket

# https://www.w3schools.com/python/ref_string_format.asp
# https://docs.python.org/3/library/pathlib.html
# https://dev.to/itsmycode/how-to-get-hostname-in-python-1981#:~:text=Syntax%20%E2%80%93%20socket.gethostname(),the%20machine%20in%20string%20format.
# Validate file
def fileValidator(supportedFileTypes, filePath):
    path = Path(filePath)
    # Check for validity
    if path.exists() and path.is_file():
        if path.suffix not in supportedFileTypes:
            print(bcolors.FAIL + f"Unsupported file type: {path.suffix}" + bcolors.ENDC)
            exit()
    else:
        print(bcolors.FAIL + f"Invalid file path: {path}" + bcolors.ENDC)
        exit()
    return path

def fileCreator(supportedFileTypes, filePath):
    path = Path(filePath)
    if path.suffix not in supportedFileTypes:
        print(bcolors.FAIL + f"Unsupported file type: {path.suffix}" + bcolors.ENDC)
        exit()
    else:
        with open(filePath, "w") as f:
            pass
        return path

# Validate stream
def streamValidator(supportedStreams, streamName):
    if streamName not in supportedStreams:
        print(bcolors.FAIL + f"Invalid Stream: {streamName}" + bcolors.ENDC)
        exit()
    else:
        return streamName

# Validate selection
def selectionValidator(selection):
    selection = str.upper(selection)
    allowed = ["Y","YES","N","NO"]
    if selection not in allowed:
        print(bcolors.FAIL + f"Invalid Selection: {selection}" + bcolors.ENDC)
        exit()
    else:
        return True

# Get user input for blockchain config
def dataConfig():
    # declare supported filetypes
    supportedFileTypes = [".log",".csv"]
    supportedStreams = ["data"]
    # Get the FilePath and fileName
    filePath = input(bcolors.WARNING + f"Enter Path to Log File:"+bcolors.OKBLUE+ f"\n:")
    filePath = fileValidator(supportedFileTypes, filePath)

    # Get copy path
    copyPath = input(bcolors.WARNING + f"Enter Path for Copy File:"+bcolors.OKBLUE+ f"\n:")
    copyPath = fileCreator(supportedFileTypes, copyPath)

    # Get the name of the file
    fileType = filePath.name
    streamName = input(bcolors.WARNING + f"Select Stream: {supportedStreams}"+bcolors.OKBLUE+ f"\n:")
    streamName = streamValidator(supportedStreams, streamName)
    # Get the current system
    key = socket.gethostname()
    # Selector for listener
    selection = input(bcolors.WARNING + f"Start File Listener: y/n\n" + bcolors.ENDC)
    selection = selectionValidator(selection)
    
    print(bcolors.OKGREEN, filePath, fileType, streamName, key, bcolors.ENDC)
    return filePath, fileType, streamName, key, selection, copyPath

def getPassword():
    password = input(bcolors.WARNING + "Enter Password: " + bcolors.ENDC)
    return password