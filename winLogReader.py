from mcController import getStreamData

# Writing data to a file
def writeToFile(file, data):
    with open(file,"wb") as f:
        f.write(data)

# Get the data from sthe stream
streamData = getStreamData("data", False)

# Write current state of chain to json
writeToFile("streamData.json", streamData)

# Read through the json file
# Decrypt each JSON entry
# Save decrypted data to file

