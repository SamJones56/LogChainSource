# from aesController import decAes
import hashlib

# kyberCipherTextHex = ""
# nonceHex = ""
# cipherTextHex = ""
# tag = ""

# decrypted = decAes(kyberCipherTextHex, nonceHex, cipherTextHex, tag)

# print(decrypted)

# with open("csv/linTest.csv", "rb") as f:
#     digest = hashlib.file_digest(f, "sha256")

# print(digest.hexdigest())


# Initial data read from file -> go through file and for each entry: fileHash, data encryption, coversion, posting
# Constant data listener -> changes in file: fileHash, data encryption, conversion, posting
# Hash digest of file 
# Encrypt data
# Convert data to blockchain JSON
# Upload to chain

# Method for building windows JSON
# def winLog(row,key):
#     return {"json":{
#         "Node": key,
#         "Type": "Windows",
#         "LogId" : row['LineId'],
#         "Date":row['Date'],
#         "Time":row['Time'],
#         "Level":row['Level'],
#         "Component":row['Component'],
#         "Content":row['Content'],
#         "EventId":row['EventId'],
#         "EventTemplate":row['EventTemplate'],
#         }}

# Method for building linux JSON
# def linLog(row,key):
#     return {"json":{
#         "Node": key,
#         "Type": "Linux",
#         "LineId" : row['LineId'],
#         "Date":row['Date'],
#         "Time":row['Time'],
#         "Level":row['Level'],
#         "Component":row['Component'],
#         "PID":row['PID'],
#         "Content":row['Content'],
#         "EventId":row['EventId'],
#         "EventTemplate":row['EventTemplate'],
#         }}

# https://docs.python.org/3/library/csv.html
# Parse through the csv
# def postToChain(fileName, fileType, streamName, key):
#     with open(fileName, newline='') as csvfile:
#         reader = csv.DictReader(csvfile)
#         for row in reader:
#             # if fileType == 1:
#             #     # log = winLog(row,key)
#             #     log = logJ(row,key,"Windows")
#             #     # print(row,key)
#             # elif fileType == 2:
#             #     # log = linLog(row,key)
#             #     log = logJ(row,key,"Linux")
#             # json to binary for encryption
#             # stringLog=json.dumps(log)

#             binaryLog=stringLog.encode('utf-8')

#             # Get kyber shared secret and ciphertext
#             kCipherText, ksharedsecret = encapsulate(publicKey)
#             # Set the key for AES as the generated shared secret from kyber
#             aesKey = ksharedsecret
#             # AES encrypt the log using hashed kyber generated shared secret
#             nonce,cipherText,tag = encAes(binaryLog, aesKey)

#             # Data for posting to data stream
#             data = {"json":{
#                 "kyberct":kCipherText.hex(),
#                 "nonce":nonce.hex(),
#                 "data":cipherText.hex(),
#                 "tag":tag.hex()}}

#             # Add to the data stream
#             print(bcolors.WARNING + "Ammending ", end=" ")
#             print(log, end=" ")
#             print(" to Chain" + bcolors.ENDC)
#             addToStream(streamName, key, data)


from userInterface import dataConfig

dataConfig()