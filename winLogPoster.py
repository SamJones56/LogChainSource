from mcController import addToStream
import csv
import time
import json
from colours import bcolors
# https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9
from random import randrange
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
from aesController import encAes
# https://medium.com/@hwupathum/using-crystals-kyber-kem-for-hybrid-encryption-with-java-0ab6c70d41fc
from kyberController import encapsulate, readFromFile


pkFile="kPk.key"
publicKey = readFromFile(pkFile)
streamName = "data"
key = "Windows"

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
            # Set the key for AES as the generated shared secret from kyber
            aesKey = ksharedsecret
            # AES encrypt the log using hashed kyber generated shared secret
            nonce,cipherText,tag = encAes(binaryLog, aesKey)

            # Convert to hex for saving to chain
            kCipherText = kCipherText.hex()
            nonce = nonce.hex()
            cipherText = cipherText.hex()
            tag = tag.hex()
            
            # Data for posting to data stream
            data = {"json":{"kyberct":kCipherText,"nonce":nonce, "data":cipherText, "tag":tag}}

            # Add to the data stream
            print(bcolors.WARNING + "Ammending ", end=" ")
            print(log, end=" ")
            print(" to Chain" + bcolors.ENDC)
            addToStream(streamName, key, data)
            # addToStream(streamName, key, log)

postToChain()
