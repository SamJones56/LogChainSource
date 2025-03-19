from mcController import getStreamData
from aesController import decAes
import json
import time
# https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
# Writing data to a file
def writeToFile(file, data):
    with open(file,"w") as f:
        json.dump(data, f)

# Read and decrypt
def readDecryptSave(file):
    with open(file, "r") as f:
        jsonOut = json.load(f)
    # Store output
    jDecrypted = []
    # Loop through the json output
    for x in jsonOut:
        print(x)
        # Gather info from json
        jLine = x["data"]["json"]
        # publisher = jLine["publisher"]
        kyberct = jLine["kyberct"]
        nonce = jLine["nonce"]
        cipherText = jLine["data"]
        tag = jLine["tag"]

        # Decrypt the json
        jDecrypt = decAes(kyberct,nonce,cipherText,tag)

        # Append to jDecrypted
        jDecrypted.append(jDecrypt)
    # Save the final list    
    writeToFile("streamDataDec.json", jDecrypted)


# Get the data from sthe stream
streamData = getStreamData("data", False)

# Write current state of chain to json
writeToFile("streamDataEnc.json", streamData)
# time.sleep(20)
readDecryptSave("streamDataEnc.json")
