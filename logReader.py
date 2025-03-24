from mcController import getStreamData
from aesController import decAes
from colours import bcolors
from compareCheck import logCompare
import json
import time


def readDecryptSave(fileName, streamName):
    # Get stream data
    streamData = getStreamData(streamName, False)
    for line in streamData:
        encrypted = line["data"]["json"]
        # Decrypt
        decrypted = decAes(encrypted["kyberct"],
                           encrypted["nonce"],
                           encrypted["log"],
                           encrypted["tag"])
        data = {
            "WalletAddress":line["publishers"],
            "Node":line["Keys"],
            "TransactionID":line["txid"],
            "json":decrypted
        }
        with open(fileName, "a") as f:
            f.write(json.dumps(data))
        # output.append(data)
        




readDecryptSave("streamDataEnc.json", "data")