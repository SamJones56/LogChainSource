# This python class will be used to generate and post to stream the kyber public key
from pqcrypto.kem.kyber512 import generate_keypair, encrypt, decrypt
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

# Get pubkey
def getPubKey():
    with open(pkFile,"rb") as f:
        return f.read()

# Generate and save private/public keys ~ TODO make files private
def genKeys():
    # Generate kyber keys
    pk,sk = generate_keypair()
    # Write keys to file
    writeToFile(pkFile, pk)
    writeToFile(skFile, sk)
    print(bcolors.OKGREEN + "Wrote keys to files: " + pkFile + skFile + bcolors.ENDC)


# Encrypt data
def encryptData(data):
    pk = getPubKey()
    return encrypt(pk,data)

# Decrypt data
def decryptData(data):
    return decrypt(data)
