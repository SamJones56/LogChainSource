# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
# https://medium.com/@hwupathum/using-crystals-kyber-kem-for-hybrid-encryption-with-java-0ab6c70d41fc
import hashlib
from mcController import addToStreamOptions

# Get pubkey
def readFromFile(file):
    with open(file,"rb") as f:
        return f.read()

pkFile="kPk.key"
publicKey = readFromFile(pkFile)

# Writing data to a file
def writeToFile(file, data):
    with open(file,"wb") as f:
        f.write(data)

def appendToFile(file,data):
    with open(file,"a") as f:
        f.write(data)
    
# Copy log 
def saveCopy(filePath, line):
    with filePath.open("w") as file:
        file.write(line)

# https://docs.python.org/3/library/hashlib.html
# Get the hash of the log file
def getFileHash(fileName):
    with open(fileName, "rb") as f:
        digest = hashlib.file_digest(f,"sha256")
    return digest.hexdigest()

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

# https://www.w3schools.com/python/ref_file_readlines.asp
def compareLogs(copyPath, filePath):
    with copyPath.open("r") as copy, filePath.open("r") as current:
        copySet = set(copy.readlines())
        currentSet = set(current.readlines())
        diff = copySet ^ currentSet
        if diff:
            return diff