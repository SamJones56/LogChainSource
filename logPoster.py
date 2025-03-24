from mcController import addToStreamOptions
import hashlib
# https://docs.python.org/3/library/pathlib.html
from userInterface import dataConfig
from colours import bcolors
# https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9
from random import randrange
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
from aesController import encAes
# https://medium.com/@hwupathum/using-crystals-kyber-kem-for-hybrid-encryption-with-java-0ab6c70d41fc
from kyberController import encapsulate, readFromFile
import threading
import time

pkFile="kPk.key"
publicKey = readFromFile(pkFile)

# https://docs.python.org/3/library/hashlib.html
# Get the hash of the log file
def getFileHash(fileName):
    with open(fileName, "rb") as f:
        digest = hashlib.file_digest(f,"sha256")
    return digest.hexdigest()

# data -> JSON for blockchain
def blockConverter(fileType,hashDigest,log):
    # Data for identification
    entry = {
        "Type":fileType,
        "FileHash":hashDigest,
    }
    entry.update(log)
    return entry

# Convert log to binary, encrypt with AES, return JSON data for upload
def logEncryptor(log):
    # Convert log to binary
    binaryLog = log.encode('utf-8')
    # Get kyber shared secret and ciphertext
    kCipherText, ksharedsecret = encapsulate(publicKey)
    # AES encrypt the log using hashed kyber generated shared secret
    nonce,cipherText,tag = encAes(binaryLog, ksharedsecret)
    # Data for posting to data stream
    data = {
        "kyberct":kCipherText.hex(),
        "nonce":nonce.hex(),
        "log":cipherText.hex(),
        "tag":tag.hex()}
    return data

# Get encrypted data and upload to chain
def postToChain(key, fileType, hashDigest, log, streamName):
    data = blockConverter(fileType,hashDigest,log)
    # Add to the data stream
    data = {"json":data}
    addToStreamOptions(streamName, key, data, "offchain")

def listener(key, fileType, hashDigest, log, streamName):
    x = 0
    while x < 0:
        print("test")
        time.sleep(5)
        x += 1 

# Initial upload of file to blockchain
def initialUpload():
    # Get user input
    filePath, fileType, streamName, key, selection = dataConfig()
    # Get file hash
    hashDigest = getFileHash(filePath)
    # Read log file line by line posting each to stream
    with filePath.open("r") as logFile:
        for logLine in logFile:
            # Encrypt log
            log = logEncryptor(logLine)
            # Post to stream
            print(bcolors.WARNING + f"Ammending to {streamName} Stream\n" + bcolors.OKBLUE + f"{logLine}" + bcolors.ENDC)
            postToChain(key, fileType, hashDigest, log, streamName)
    # Check for selection
    if selection:
        t = threading.Thread(target=listener, args=(key, fileType, hashDigest, log, streamName))  
        # https://www.instructables.com/How-to-Communicate-and-Share-Data-Between-Running-/
        t.start(listener)

initialUpload()

# This should be its own python file
# def liveReader():

# fileName,fileType,streamName,key = usrInput()

# postToChain(fileName,fileType,streamName,key)