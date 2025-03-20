from mcController import getStreamData
from aesController import decAes
from colours import bcolors
import json
import time
# https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
# Writing data to a file
def writeToFile(file, data):
    with open(file,"w") as f:
        json.dump(data, f)

# Read and decrypt
def readDecryptSave(jsonOut):
    # with open(file, "r") as f:
    #     jsonOut = json.load(f)
    # Store output
    jDecrypted = []
    # Loop through the json output
    for jLine in jsonOut:
        key = jLine["keys"]
        # Gather info from json
        jData = jLine["data"]["json"]
        kyberct = jData["kyberct"]
        nonce = jData["nonce"]
        cipherText = jData["data"]
        tag = jData["tag"]

        # Decrypt the json
        jDecrypt = decAes(kyberct,nonce,cipherText,tag)
        # Tag the decrypted data with the key
        data = key , jDecrypt
        
        # Append to jDecrypted
        jDecrypted.append(data)
    # Save the final list    
    writeToFile("streamDataDec.json", jDecrypted)

# Get the data from sthe stream
streamData = getStreamData("data", False)
readDecryptSave(streamData)
# Write current state of chain to json
# writeToFile("streamDataEnc.json", streamData)
# time.sleep(10)
# Decrypt json state
# readDecryptSave("streamDataEnc.json")
