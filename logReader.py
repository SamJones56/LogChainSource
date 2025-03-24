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
        try:
            encrypted = line["data"]["json"]
            # Decrypt
            # print(
            #     encrypted["kyberct"],
            #     encrypted["nonce"],
            #     encrypted["log"],
            #     encrypted["tag"]
            # )
            decrypted = decAes(encrypted["kyberct"],
                                encrypted["nonce"],
                                encrypted["log"],
                                encrypted["tag"]
            )
            print(decrypted)
            if decrypted is None:
                print(bcolors.FAIL + f"FAIL TXID: {line['txid']}" + bcolors.ENDC)
            data = {
                "WalletAddress":line["publishers"],
                "Node":line["keys"],
                "TransactionID":line["txid"],
                "json":decrypted
            }
            with open(fileName, "a") as f:
                f.write(json.dumps(data))
        except Exception as e:
            print(f"{e}")
        

readDecryptSave("streamDataEnc.json", "data")
