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

# https://likegeeks.com/count-json-array-elements-python/#:~:text=7%20Benchmark%20Test-,Using%20len()%20Function,arrays%20>
# https://www.w3schools.com/python/python_lists_comprehension.asp
def logCompare(fileName):
    # Valid for Windows
    with open(fileName,"r") as f:
        # Read from json
        jsonOut = json.load(f)
        # Declare list of id's
        ids = []

        # Get windows logs
        winLogs = [jData for jData in jsonOut if jData["data"]["Type"]=="Windows"]
        print(winLogs)



        # # Loop through JSON lines in JSON output
        # for jLine in jsonOut:
        #     # Check if windows
        #     if jLine["data"]["Type"] == "Windows":
        #         if jLine["data"]["LogId"] not in ids:
        #             ids.append(jLine["data"]["LogId"])
        #             print(ids)
        #             test = "1"
        #             count = sum(1 for obj in jsonOut if obj["data"]["LogId"] == test)
        #             print(count)
        #     elif jLine["data"]["Type"] == "Linux":
        #         break





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