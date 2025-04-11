from mcController import getStreamData
from cryptoUtils import decAes, writeToFileEnc
from colours import bcolors
import json
# import os
# from userInterface import getPassword, selectionValidator

path = "/logChain/app/streamDataDec.json"
copyPath = "/logChain/app/streamDataEnc.json"

def readDecryptSave(fileName, copyName, streamName, keyPass, logPass, webSelection):
    # Get stream data
    streamData = getStreamData(streamName, False)
    results= []
    for line in streamData:
        # Decrypt
        try:
            encrypted = line["data"]["json"]
            # Decrypt the data
            decrypted = decAes(encrypted["kyberct"],
                                encrypted["nonce"],
                                encrypted["log"],
                                encrypted["tag"],
                                keyPass
            )
            if decrypted is None:
                print(bcolors.FAIL + f"FAIL TXID: {line['txid']}" + bcolors.ENDC)
            data = {
                "WalletAddress":line["publishers"],
                "Node":line["keys"],
                "TransactionID":line["txid"],
                "Time": encrypted["Time"],
                "FileType":encrypted["Type"],
                "FileHash":encrypted["FileHash"],
                "json":decrypted
            }
            results.append(data)
        except Exception as e:
            print(f"{e}")

    # Reading and writing from file
    # password = b"password"
    with open(fileName, "wb") as f:
        for item in results:
            # For printing to terminal
            if not webSelection:
                printLogLine(item)
            line = json.dumps(item).encode()
            f.write(line + b"\n")
    
    with open(fileName,"rb") as f:
        data = f.read()
    
    writeToFileEnc(fileName,logPass,data)



def printLogLine(data):
    added = "added:"
    removed = "removed:"
    deletion = "DELETION:"
    
    log = data.get("json", "")
    logStr = str(log)
    # If a line was removed and one was added eg. potentially a modified line
    if added in logStr and removed in logStr:
        print(bcolors.OKBLUE + "Log Edited" + bcolors.ENDC)
        print(bcolors.WARNING + f"{data}" + bcolors.ENDC)
    # Line added to log file
    elif added in logStr:
        print(bcolors.OKBLUE + "Log Added" + bcolors.ENDC)
        print(bcolors.OKGREEN + f"{data}" + bcolors.ENDC)
    # Log removed from log file
    elif removed in logStr:
        print(bcolors.OKBLUE + "Log Removed" + bcolors.ENDC)
        print(bcolors.WARNING + f"{data}" + bcolors.ENDC)
    # Log deleted from log file
    elif deletion in logStr:
        print(bcolors.OKBLUE + "File Deleted" + bcolors.ENDC)
        print(bcolors.FAIL + f"{data}" + bcolors.ENDC)
    print('─' * 10)  # U+2501, Box Drawings Heavy Horizontal





    # os.remove(fileName)

        # jdata = json.dumps(results).encode()

        # password = b"password"
        # writeToFileEnc(fileName,password,jdata)

        # with open(fileName, "w") as f:
        #     for item in results:
        #         json.dump(item,f)
        #         f.write("\n")

# filePath = input(bcolors.WARNING + f"Enter Path to Log File:"+bcolors.OKBLUE+ f"\n:")
# filePath = fileCreator(supportedFileTypes, filePath)
# readDecryptSave(filePath, "data")