# https://github.com/aabmets/quantcrypt
# https://github.com/aabmets/quantcrypt/wiki/Code-Examples
from colours import bcolors
from Crypto.Cipher import AES
from quantcrypt.kem import MLKEM_512, PQAVariant
from hashlib import pbkdf2_hmac
import os
import subprocess

kem = MLKEM_512(PQAVariant.REF)

# file locations
publicKeyFile="kPk.key"
secretKeyFile="kSk.key"

# Generate sudo files
def genSudoFile(path):
    try:
        subprocess.run(["touch",f"{path}"])
        subprocess.run(["chown","root:root",f"{path}"])
        subprocess.run(["chmod","600", f"{path}"])
        print(bcolors.OKGREEN + "Generated: " + publicKeyFile + " " + secretKeyFile + bcolors.ENDC)
    except PermissionError:
        print("Process Error")
        return None

# Get pubkey
def readFromFile(file):
    with open(file,"rb") as f:
        return f.read()

# Writing data to a file
def writeToFile(file, data):
    with open(file,"wb") as f:
        f.write(data)

# Generate and save private/public keys ~ TODO make files private
def kyberGenKeys():
    # Generate kyber keys
    pk,sk = kem.keygen()
    # Write keys to file
    writeToFile(publicKeyFile, pk)
    writeToFile(secretKeyFile, sk)
    print(bcolors.OKGREEN + "Wrote keys to files: " + publicKeyFile + secretKeyFile + bcolors.ENDC)

# Encrypt data
def kyberEncapsulate(publicKey):
    cipherText, sharedSecret = kem.encaps(publicKey)
    return cipherText, sharedSecret

# Decrypt data
def kyberDecapsulate(cipherText):
    secretKey = readFromFile(secretKeyFile)
    sharedSecret = kem.decaps(secretKey, cipherText)
    return sharedSecret

# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
def encAes(data, aesKey):
        # aes key generated from Kyber shared secret
        cipher = AES.new(aesKey, AES.MODE_EAX)
        # Generate nonce
        nonce = cipher.nonce
        # Encrypt the data
        ciphertext,tag = cipher.encrypt_and_digest(data)
        # Return nonce and ciphertext ~ to be posted to data stream
        return(nonce,ciphertext,tag)

# Decrypting AES using KyberCipherText, shared nonce, and ciphertext
def decAes(kCipherText, nonce, cipherText, tag):
        # Convert to bytes
        kCipherText = bytes.fromhex(kCipherText)
        nonce = bytes.fromhex(nonce)
        cipherText = bytes.fromhex(cipherText)
        tag = bytes.fromhex(tag)
        # Get the shared secret from the kyber ciphertext
        aesKey = kyberDecapsulate(kCipherText)
        # Decrypt AES
        cipher = AES.new(aesKey, AES.MODE_EAX, nonce=nonce)
        decrypted = cipher.decrypt(cipherText)
        try:
                # Verify tag for authenticity
                cipher.verify(tag)
                # Convert to json
                return decrypted.decode("utf-8")
        except:
                print(bcolors.FAIL + "Invalid Tag" + bcolors.ENDC)

# Convert log to binary, encrypt with AES, return JSON data for upload
def logEncryptor(log):
    # Convert log to binary
    binaryLog = log.encode('utf-8')
    publicKey = readFromFile(publicKeyFile)
    # Get kyber shared secret and ciphertext
    kCipherText, ksharedsecret = kyberEncapsulate(publicKey)
    # AES encrypt the log using hashed kyber generated shared secret
    nonce,cipherText,tag = encAes(binaryLog, ksharedsecret)
    # Data for posting to data stream
    data = {
        "kyberct":kCipherText.hex(),
        "nonce":nonce.hex(),
        "log":cipherText.hex(),
        "tag":tag.hex()}
    return data

# https://docs.python.org/3/library/hashlib.html
def fileEncryptor(path, password):
    # Generate hash of password for bcrypt
    salt = os.urandom(16)
    # Number of iteration
    iterations = 500_000
    dk = pbkdf2_hmac()