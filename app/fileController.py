# Writing data to a file
def writeToFile(file, data):
    with open(file,"wb") as f:
        f.write(data)

# Get pubkey
def readFromFile(file):
    with open(file,"rb") as f:
        return f.read()