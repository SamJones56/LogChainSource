from mcController import getStreamData
from aesController import decAes
from colours import bcolors
from compareCheck import logCompare
import json
import time


def readDecryptSave(fileName, streamName):
    # Get stream data
    streamData = getStreamData(streamName, False)
    # init output
    # output = []
    # Get json data
    for line in streamData:
        
        # Decrypt
        decrypted = decAes(line["data"]["json"]["kyberct"],
                           line["data"]["json"]["nonce"],
                           line["data"]["json"]["log"],
                           line["data"]["json"]["tag"])
        data = {
            "WalletAddress":line["publishers"],
            "Node":line["Keys"],
            "TransactionID":line["txid"],
            "json":decrypted
        }
        with open(fileName, "a") as f:
            f.write(f"{data}\n")
        # output.append(data)
        




readDecryptSave("streamDataEnc.json", "data")