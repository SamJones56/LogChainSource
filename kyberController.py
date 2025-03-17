# This python class will be used to generate and post to stream the kyber public key
# https://github.com/aabmets/quantcrypt/wiki/Code-Examples
from quantcrypt.kem import MLKEM_512

kyber = MLKEM_512()

class bcolors:
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

# file locations
publicKeyFile="kPk.key"
secretKeyFile="kSk.key"

# Writing data to a file
def writeToFile(file, data):
    with open(file,"wb") as f:
        f.write(data)

# Get pubkey
def readFromFile(file):
    with open(file,"rb") as f:
        return f.read()

# # Generate and save private/public keys ~ TODO make files private
def genKeys():
    # Generate kyber keys
    pk,sk = kyber.keygen()
    # Write keys to file
    writeToFile(publicKeyFile, pk)
    writeToFile(secretKeyFile, sk)
    print(bcolors.OKGREEN + "Wrote keys to files: " + publicKeyFile + secretKeyFile + bcolors.ENDC)

# Encrypt data
def encapsulate(publicKey):
    cipherText, sharedSecret = kyber.encaps(publicKey)
    return cipherText, sharedSecret

# Decrypt data
def decapsulate(cipherText):
    secretKey = readFromFile(secretKeyFile)
    sharedSecret = kyber.decaps(secretKey, cipherText)
    return sharedSecret
