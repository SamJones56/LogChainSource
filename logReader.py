from mcController import getStreamData
from aesController import decAes
from colours import bcolors
from compareCheck import logCompare
import json
import time
# https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
# Writing data to a file
def writeToFile(file, data):
    with open(file,"w") as f:
        json.dump(data, f)

# Read and decrypt
def readDecryptSave(jsonOut):
    # Store output
    jDecrypted = []
    # Loop through the json output
    for jLine in jsonOut:
        # Get the publishers and keys
        publishers = jLine['publishers']
        key = jLine["keys"]
        # Gather info from json
        jData = jLine["data"]["json"]
        kyberct = jData["kyberct"]
        nonce = jData["nonce"]
        cipherText = jData["data"]
        tag = jData["tag"]

        # Decrypt the json
        jDecrypt = decAes(kyberct,nonce,cipherText,tag)
        # Remove nested
        if "json" in jDecrypt:
            jDecrypt=jDecrypt["json"]
        
        data = {
            "walletAddress":publishers,
            "nodeKey":key,
            "data":jDecrypt
        }
        
        # Append to jDecrypted
        jDecrypted.append(data)
    # Save the final list    
    writeToFile("streamDataDec.json", jDecrypted)

# Get the data from sthe stream
streamData = getStreamData("data", False)
readDecryptSave(streamData)
logCompare("streamDataDec.json")

# "reload button" clicked -> 
# 1. Call -> streamData = getStreamData("data", False)  :: Gets current data stream data 
# 2. readDecryptSave(streamData)                        :: Decryptes the data stream and saves it to "streamDataDec.json"
# Extra. logCompare("streamDataDec.json")               :: Is how we compare the decoded json file