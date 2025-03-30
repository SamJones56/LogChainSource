# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
# https://medium.com/@hwupathum/using-crystals-kyber-kem-for-hybrid-encryption-with-java-0ab6c70d41fc
import hashlib
from mcController import addToStreamOptions
from pathlib import Path

def appendToFile(file,data):
    with open(file,"a") as f:
        f.write(data)
    
# Copy log 
# https://www.geeksforgeeks.org/python-seek-function/
def saveCopy(copyPath, filePath):
    copyPath = Path(copyPath)
    filePath = Path(filePath)
    with filePath.open("r") as file, copyPath.open("w") as copy:
        file.seek(0)
        copy.writelines(file.readlines())

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

# Get last line in files
# for line in tail("-n 1",filePath, _iter=True):
def endOfFile(filePath):
    with open(filePath, "r") as f:
        lines = f.readlines()
        return lines[-1]


# https://www.w3schools.com/python/ref_file_readlines.asp
def compareLogs(copyPath, filePath):
    flag = False
    with open(copyPath,"r") as copy, open(filePath, "r") as current:
        # Get the lines
        copyLines = copy.readlines()
        currentLines = current.readlines()
    # Get the length
    copyCount = len(copyLines)
    currentCount = len(currentLines)

    # Get and compare sets
    copySet = set(copyLines)
    currentSet = set(currentLines)
    # Get difference
    diff = copySet ^ currentSet

    # Line deletion detection
    if currentCount<copyCount:
        flag=True
        print("line deletion detected")
        return(diff, flag)
    elif diff and currentCount == copyCount:
        print("edit detected")
        return diff,flag
    elif diff and currentCount != copyCount:
        flag = True
        print("edit and deletion detected")
        return diff, flag