# This python class will be used to generate and post to stream the kyber public key
# https://github.com/aabmets/quantcrypt
# https://github.com/aabmets/quantcrypt/wiki/Code-Examples
from colours import bcolors
from fileController import writeToFile, readFromFile
from quantcrypt.kem import MLKEM_512, PQAVariant

kem = MLKEM_512(PQAVariant.REF)

# file locations
publicKeyFile="kPk.key"
secretKeyFile="kSk.key"

# # Generate and save private/public keys ~ TODO make files private
def genKeys():
    # Generate kyber keys
    pk,sk = kem.keygen()
    # Write keys to file
    writeToFile(publicKeyFile, pk)
    writeToFile(secretKeyFile, sk)
    print(bcolors.OKGREEN + "Wrote keys to files: " + publicKeyFile + secretKeyFile + bcolors.ENDC)

# Encrypt data
def encapsulate(publicKey):
    cipherText, sharedSecret = kem.encaps(publicKey)
    return cipherText, sharedSecret

# Decrypt data
def decapsulate(cipherText):
    secretKey = readFromFile(secretKeyFile)
    sharedSecret = kem.decaps(secretKey, cipherText)
    return sharedSecret
