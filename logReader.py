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

# https://likegeeks.com/count-json-array-elements-python/#:~:text=7%20Benchmark%20Test-,Using%20len()%20Function,arrays%20are%20represented%20in%20Python.
# https://likegeeks.com/count-json-array-elements-python/#:~:text=7%20Benchmark%20Test-,Using%20len()%20Function,arrays%20>
def logCompare(fileName):
    with open(fileName,"r") as f:
        jsonOut = json.load(f)
    # for jLine in jsonOut:
        test = "1"
        #test = "LogId"
        # positive_feedback_count = sum(1 for obj in data if obj['feedback'] in ["Very satisfied", "Satisfied"])
        count = sum(1 for obj in jsonOut if obj["data"]["LogId"] == test)
        print(count)


# Read and decrypt
def readDecryptSave(jsonOut):
    # with open(file, "r") as f:
    #     jsonOut = json.load(f)
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
# Write current state of chain to json
# writeToFile("streamDataEnc.json", streamData)
# time.sleep(10)
# Decrypt json state
# readDecryptSave("streamDataEnc.json")
logCompare("streamDataDec.json")