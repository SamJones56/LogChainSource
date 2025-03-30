# https://docs.python.org/3/library/pathlib.html
from userInterface import dataConfig
from colours import bcolors
from utils import getFileHash, postToChain, saveCopy
from cryptoUtils import logEncryptor
# Watchdog
from watchDog import doggy
import json

# Initial upload of file to blockchain
def initialUpload():
    # Get user input
    filePath, fileType, streamName, key, selection, copyPath = dataConfig()
    # Get file hash
    hashDigest = getFileHash(filePath)
    # Save a opy of the log file
    print(bcolors.WARNING + f"Saving copy: {filePath} to {copyPath}\n" + bcolors.ENDC)
    saveCopy(copyPath, filePath)
    # Read log file line by line posting each to stream
    with filePath.open("r") as logFile:
        for logLine in logFile:
            logLine = {"added:":logLine}
            logLine = json.dumps(logLine)
            # Encrypt log
            log = logEncryptor(logLine)
            # Post to stream
            print(bcolors.WARNING + f"Ammending to {streamName} Stream\n" + bcolors.OKBLUE + f"{logLine}" + bcolors.ENDC)
            postToChain(key, fileType, hashDigest, log, streamName)
    # Check for selection
    if selection:
        doggy(filePath ,fileType, key, streamName, copyPath)

initialUpload()