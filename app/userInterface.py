from colours import bcolors
from pathlib import Path
import socket
from getpass import getpass
# https://pypi.org/project/password-strength/
from password_strength import PasswordPolicy
import os

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
    elif selection == "Y":
        return True
    else:
        return False

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

    # Uploal all
    uploadAll = input(bcolors.WARNING + f"Upload Entire File: y/n\n" + bcolors.ENDC)
    uploadAll = selectionValidator(uploadAll)

    # Selector for listener
    selection = input(bcolors.WARNING + f"Start File Listener: y/n\n" + bcolors.ENDC)
    selection = selectionValidator(selection)
    
    return filePath, fileType, streamName, key, selection, copyPath, uploadAll

# https://stackoverflow.com/questions/9202224/getting-a-hidden-password-input
# https://pypi.org/project/password-strength/
policy = PasswordPolicy.from_names(
        length = 8,
        uppercase=1,
        numbers=2,
    )
def getPassword(prompt, access):
    # Skip password prompts in dev mode: set file+log encryption pwds as standard, close app, enter following (still inside genesis /app):
    # DEV_NO_PROMPT=1
    # export KEY_PASS="YourPassword1”
    # export LOG_PASS="YourPassword2”
    if os.environ.get("DEV_NO_PROMPT"):
        # Return stored env var as bytes
        return os.environ.get("KEY_PASS" if access else "LOG_PASS").encode()

    global policy
    rePrompt = bcolors.WARNING + "Please re-enter: " + bcolors.ENDC
    rules = {
        "length": 8,
        "uppercase":1,
        "numbers":2,
    }
    print(bcolors.WARNING + "Password Policy: ")
    for rule, value in rules.items():
        print(f"{rule}: {value}")
    print(bcolors.ENDC)
    while True:
        password = getpass(prompt)
        if not access:
            rePassword = getpass(rePrompt)
        issues = policy.test(password)
        if not access and password != rePassword:
            issues.append("Password missmatch")
        if issues:
            print(bcolors.FAIL + f"Password Failed on {issues}" + bcolors.ENDC)
        else:
            print(bcolors.OKGREEN + "Password Accepted!" + bcolors.ENDC)
            return password.encode()
        

    