# https://www.w3schools.com/python/python_classes.asp

class LogEntry:
    # Constructor
    def __init__(self, walletAddress, node, transactionid, time, fileType, fileHash, json):
        self.walletAddress = walletAddress
        self.node = node
        self.transactionid = transactionid
        self.time = time
        self.fileType = fileType
        self.fileHash = fileHash
        self.json = json

        
    # Return for all
    def __str__(self):
        return{
            "WalletAddress":{self.walletAddress},
            "Node":{self.node}
        }