from mcController import addToStream
import csv
import time
import json
# https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9
from random import randrange
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
from aesController import encAes
from kyberController import encapsulate, readFromFile
import hashlib

# Colours for printing
class bcolors:
    WARNING = '\033[93m'
    ENDC = '\033[0m'

pkFile="kPk.key"
publicKey = readFromFile(pkFile)
streamName = "data"
key = "node1"

# https://docs.python.org/3/library/csv.html
# Parse through the csv
def postToChain():
    with open('winTest.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Simulate random time
            t = randrange(6)
            time.sleep(t)
            # Generate the json file
            log = {"json":{"LogId" : row['LineId'],
                        "Date":row['Date'],
                        "Time":row['Time'],
                        "Level":row['Level'],
                        "Component":row['Component'],
                        "Content":row['Content'],
                        "EventId":row['EventId'],
                        "EventTemplate":row['EventTemplate'],
                        }}
            # json to binary for encryption
            stringLog=json.dumps(log)
            binaryLog=stringLog.encode('utf-8')

            # Get kyber shared secret and ciphertext
            kCipherText, ksharedsecret = encapsulate(publicKey)
            # Set the key for AES as the generated shared secret from kyber ~ SHA guarantees proper length
            # https://docs.python.org/3/library/hashlib.html
            # aesKey = hashlib.sha256(ksharedsecret).digest()
            aesKey = ksharedsecret
            # AES encrypt the log using hashed kyber generated shared secret
            nonce,cipherText = encAes(binaryLog, aesKey)

            # Convert to hex for saving to chain
            kCipherText = kCipherText.hex()
            nonce = nonce.hex()
            cipherText = cipherText.hex()
            
            # Data for posting to data stream
            data = {"json":{"kyberct":kCipherText,"nonce":nonce, "data":cipherText}}
            # Add to the data stream
            print(bcolors.WARNING + "Ammending ", end=" ")
            print(log, end=" ")
            print(" to Chain" + bcolors.ENDC)
            addToStream(streamName, key, data)

postToChain()