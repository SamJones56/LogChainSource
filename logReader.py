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
    output = []
    # Get json data
    for line in streamData:
        kyberct = line["data"]["kyberct"]
        nonce = line["data"]["nonce"]
        cipherText = line["data"]["log"]
        tag = line["data"]["tag"]
        txid = line["txid"]
        # Decrypt
        decrypted = decAes(kyberct,nonce,cipherText,tag)

        transactionData = {
            "WalletAddress":line["publishers"],
            "Node":line["Keys"],
            "TransactionID":line["txid"]
        }




readDecryptSave("streamDataEnc.json", "data")