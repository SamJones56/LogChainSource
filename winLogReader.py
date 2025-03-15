from mcController import connectToChain, subStream, grantStream, addToStream ,getStreamData
import csv
import time
# https://stackoverflow.com/questions/3996904/generate-random-integers-between-0-and-9
from random import randrange
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
from encAES import encAes
# LineId,Date,Time,Level,Component,Content,EventId,EventTemplate

pkFile="kPk.key"

# Colours for printing
class bcolors:
    WARNING = '\033[93m'
    ENDC = '\033[0m'

streamName = "data"
key = "node1"

# https://docs.python.org/3/library/csv.html
# Parse through the csv
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
        # Encrypt the log and return key, nonce, and ciphertext
        key,nonce,ciphertext = encAes(log)

        # Encrypt the 

        # Print out what we are doing
        print(bcolors.WARNING + "Ammending ", end=" ")
        print(log, end=" ")
        print(" to Chain" + bcolors.ENDC)
        addToStream(streamName, key, ct)

