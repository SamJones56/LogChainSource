from mcController import getStreamData
from aesController import decAes
from colours import bcolors
# from compareCheck import logCompare
import json


def readDecryptSave(fileName, streamName):
    # Get stream data
    streamData = getStreamData(streamName, False)
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
                "FileHash":encrypted["FileHash"],
                "json":decrypted
            }
            with open(fileName, "a") as f:
                
                json.dump(data,f)
   
        except Exception as e:
            print(f"{e}")
        

# readDecryptSave("streamDataDec.txt", "data")
