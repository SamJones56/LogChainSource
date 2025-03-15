# This python class will be used to generate and post to stream the kyber public key
from kyber_py.kyber import Kyber512
import os

class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

# file locations
pkFile="kPk.key"
skFile="kSk.key"

# Writing data to a file
def writeToFile(file, data):
    with open(file,"wb") as f:
        f.write(data)

# Generate and save private/public keys ~ TODO make files private
def genKeys():
    # Generate kyber keys
    pk,sk = Kyber512.keygen()
    # Write keys to file
    writeToFile(pkFile, pk)
    writeToFile(skFile, sk)
    print(bcolors.OKGREEN + "Wrote keys to files: " + pkFile + skFile + bcolors.ENDC)

# Get pubkey
def getPubKey():
    with open(pkFile,"rb") as f:
        return f.read()