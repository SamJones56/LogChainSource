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
            decrypted = decAes(encrypted["kyberct"],
                                encrypted["nonce"],
                                encrypted["data"],
                                encrypted["tag"]
            )
            if decrypted is None:
                print(bcolors.FAIL + f"[FAIL] TXID: {line['txid']}" + bcolors.ENDC)

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
        

# Run it
readDecryptSave("streamDataEnc.json", "data")



readDecryptSave("streamDataEnc.json", "data")