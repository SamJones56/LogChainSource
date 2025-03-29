# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
from aesController import encAes
# https://medium.com/@hwupathum/using-crystals-kyber-kem-for-hybrid-encryption-with-java-0ab6c70d41fc
from kyberController import encapsulate, readFromFile
import hashlib
from mcController import addToStreamOptions

pkFile="kPk.key"
publicKey = readFromFile(pkFile)

# https://docs.python.org/3/library/hashlib.html
# Get the hash of the log file
def getFileHash(fileName):
    with open(fileName, "rb") as f:
        digest = hashlib.file_digest(f,"sha256")
    return digest.hexdigest()

# Convert log to binary, encrypt with AES, return JSON data for upload
def logEncryptor(log):
    # Convert log to binary
    binaryLog = log.encode('utf-8')
    # Get kyber shared secret and ciphertext
    kCipherText, ksharedsecret = encapsulate(publicKey)
    # AES encrypt the log using hashed kyber generated shared secret
    nonce,cipherText,tag = encAes(binaryLog, ksharedsecret)
    # Data for posting to data stream
    data = {
        "kyberct":kCipherText.hex(),
        "nonce":nonce.hex(),
        "log":cipherText.hex(),
        "tag":tag.hex()}
    return data

# data -> JSON for blockchain
def blockConverter(fileType,hashDigest,log):
    # Data for identification
    entry = {
        "Type":fileType,
        "FileHash":hashDigest,
    }
    entry.update(log)
    return entry

# Get encrypted data and upload to chain
def postToChain(key, fileType, hashDigest, log, streamName):
    data = blockConverter(fileType,hashDigest,log)
    # Add to the data stream
    data = {"json":data}
    print("added")
    addToStreamOptions(streamName, key, data, "offchain")