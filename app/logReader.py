from mcController import getStreamData
from cryptoUtils import decAes
from colours import bcolors
from userInterface import fileCreator
import json

# supportedFileTypes = [".json"]

def readDecryptSave(fileName, streamName):
    # Get stream data
    streamData = getStreamData(streamName, False)
    results= []
    for line in streamData:
        # Decrypt
        try:
            encrypted = line["data"]["json"]
            decrypted = decAes(encrypted["kyberct"],
                                encrypted["nonce"],
                                encrypted["log"],
                                encrypted["tag"]
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
        
        with open(fileName, "w") as f:
            for item in results:
                json.dump(item,f)
                f.write("\n")

# filePath = input(bcolors.WARNING + f"Enter Path to Log File:"+bcolors.OKBLUE+ f"\n:")
# filePath = fileCreator(supportedFileTypes, filePath)
# readDecryptSave(filePath, "data")