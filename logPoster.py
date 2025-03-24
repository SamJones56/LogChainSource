from mcController import addToStream
import hashlib
# https://docs.python.org/3/library/pathlib.html
from pathlib import Path
import csv
import time
import json
from colours import bcolors
# https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9
from random import randrange
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
from aesController import encAes
# https://medium.com/@hwupathum/using-crystals-kyber-kem-for-hybrid-encryption-with-java-0ab6c70d41fc
from kyberController import encapsulate, readFromFile

# Supported file types
# mColour = [bcolors.WARNING, bcolors.ENDC, bcolors.FAIL]
# messageSteps = ["Log Types:{i}\nSelection:", 
#                 "Select Stream:{i}\nSelection:",
#                 "Select Node{i}\nSelection:"]
# fileTypes = ["WindowsLog","LinuxLog","LinuxAuth"]
# streams = ["data"]
# fileNames = [""]
# nodes = ["Node1", "Node2"]

pkFile="kPk.key"
publicKey = readFromFile(pkFile)

# Get user input
# https://www.w3schools.com/python/ref_string_format.asp
# https://docs.python.org/3/library/pathlib.html
def usrInput():
    # declare supported filetypes
    supportedFileTypes = [".log",".csv"]
    # Get the filepath
    filePath =  input(bcolors.WARNING + f"Enter Path to Log File:\n")
    path = Path(filePath)
    fileName = path.name
    # Check for validity
    if path.exists() and path.is_file():
        if path.suffix not in supportedFileTypes:
            print(bcolors.FAIL + f"Unsupported file type: {path.suffix}" + bcolors.ENDC)

    




    # Get fileType
    fileType = input(bcolors.WARNING + f"Log Types: {fileTypes} \n Selection:" + bcolors.ENDC)
    # Check if valid
    if fileType not in fileTypes:
        print(bcolors.FAIL + f"Invalid file type: {fileType}" + bcolors.ENDC)
        exit()
    print(bcolors.OKGREEN, fileType, bcolors.ENDC)
    # Defaults
    streamName = "data"

    if fileType == 1:
        filePath = "winTest.csv"
        key = "Node1"
    elif fileType == 2:
        filePath = "linTest.csv"
        key = "Node2"
    else:
        print(bcolors.FAIL + "Invalid file type: ", fileType, bcolors.ENDC)
        exit()
    print(bcolors.OKGREEN, filePath, fileType, streamName, key, bcolors.ENDC)
    return filePath, fileType, streamName,key
####################################################################################

# https://docs.python.org/3/library/hashlib.html
# Get the hash of the log file
def getFileHash(fileName):
    with open(fileName, "rb") as f:
        digest = hashlib.file_digest(f,"sha256")
    return digest.hexdigest()

# data -> JSON for blockchain
def blockConverter(row,key,hashDigest,type):
    # Data for identification
    entry = {
        "Node":key,
        "Type":type,
        "Hash":hashDigest
    }
    # https://www.w3schools.com/python/ref_dictionary_items.asp
    for item, data in row.items():
        entry[item] = data
    print({"json":entry})
    return{"json": entry}

# Convert log to binary, encrypt with AES, return JSON data for upload
def logEncryptor(log):
    # Convert log to binary
    binaryLog = log.encode('utf-8')
    # Get kyber shared secret and ciphertext
    kCipherText, ksharedsecret = encapsulate(publicKey)
    # AES encrypt the log using hashed kyber generated shared secret
    nonce,cipherText,tag = encAes(binaryLog, ksharedsecret)
    # Data for posting to data stream
    data = {"json":{
        "kyberct":kCipherText.hex(),
        "nonce":nonce.hex(),
        "log":cipherText.hex(),
        "tag":tag.hex()}}
    return data

# Get encrypted data and upload to chain
def postToChain(log,streamName,hashDigest, key):
    data = blockConverter(log,streamName,hashDigest,key)
    # Add to the data stream
    print(bcolors.WARNING + f"Ammending: {log}" + f"\n\tto Chain: {streamName}")
    addToStream(streamName, key, data)

# Initial upload of file to blockchain
def initialUpload(fileName):
    # Get user input on data types

    with open(fileName) as logFile:
        for logLine in logFile:
            log = usrInput()

# This should be its own python file
# def liveReader():




fileName,fileType,streamName,key = usrInput()

postToChain(fileName,fileType,streamName,key)