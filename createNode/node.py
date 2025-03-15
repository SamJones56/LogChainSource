import subprocess
import re
import time
from mcController import connectToChain, subStream, grantStream, addToStream ,getStreamData

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Connect and grant permissions on an existing chain
def connectAndPerm(chainName, streamName, walletAddress):
    permissions = streamName + ".write,read"
    verbose = False
    print(bcolors.WARNING + "Subscribing to " + streamName + bcolors.ENDC)
    subStream(chainName,streamName)
    time.sleep(2)
    print(bcolors.WARNING + "Granting on " + streamName + bcolors.ENDC)
    grantStream(walletAddress ,permissions)
    time.sleep(5)
    getStreamData(streamName,verbose)


def logChainInit():
    # Connect to logChain
    print(bcolors.OKCYAN + "multichaind logChain@172.18.0.2:7010" + bcolors.ENDC)
    time.sleep(2)
    cmd = ["multichaind", "logChain@172.18.0.2:7010"]
    # subprocess.run(cmd)
    # Get the address string after connecting
    
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Extract address from output string
    # https://www.w3schools.com/python/python_regex.asp
    walletAddress = re.search(r"multichain-cli logChain grant (\w+) connect", result.stdout)
    walletAddress = walletAddress.group(1)

    # Get wallet address
    if walletAddress:
        print(bcolors.OKCYAN + f"ADDRESS FOUND: {walletAddress} " + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "ADDRESS NOT FOUND" + bcolors.ENDC)
    time.sleep(2)

    # Connect to logChain
    print(bcolors.WARNING + "Connecting to Chain" + bcolors.ENDC)
    connectToChain(walletAddress)
    time.sleep(2)

    # Start daemon
    print(bcolors.OKCYAN + "multichaind logChain -daemon" + bcolors.ENDC)
    subprocess.run(["multichaind", "logChain", "-daemon"])
    time.sleep(2)

    connectAndPerm("logChain", "pubkeys",walletAddress)
    connectAndPerm("logChain", "pubkeys",walletAddress)
    # # Connect & perm on pubkeys
    # chainName = "logChain"
    # streamName = "pubkeys"
    # verbose = False
    # print(bcolors.WARNING + "Subscribing to " + streamName + bcolors.ENDC)
    # subStream(chainName,streamName)
    # time.sleep(2)
    # # Get permissions for mainStream
    # print(bcolors.WARNING + "Granting on " + streamName + bcolors.ENDC)
    # permissions = streamName + ".write,read"
    # grantStream(walletAddress ,permissions)
    # time.sleep(5)
    # getStreamData(streamName,verbose)

    # # Connect & perm on data
    # chainName = "logChain"
    # streamName = "data"
    # print(bcolors.WARNING + "Subscribing to " + streamName + bcolors.ENDC)
    # subStream(chainName,streamName)
    # time.sleep(2)
    # # Get permissions for mainStream
    # print(bcolors.WARNING + "Granting on " + streamName + bcolors.ENDC)
    # permissions = streamName + ".write,read"
    # grantStream(walletAddress ,permissions)
    # time.sleep(5)
    # getStreamData(streamName,verbose)

    # streamName="pubkeys,items,access"
    # subStream(chainName,streamName)
    # time.sleep(2)



    # Test post to stream
    # key = "1"
    # data = {"json":{"name":"Sam"}}
    # print(bcolors.WARNING + "Adding test data to mainStream" + bcolors.ENDC)
    # addToStream(streamName, key, data)
    # time.sleep(2)

    # Get stream items
    # verbose = False
    # print(bcolors.WARNING + "Getting Stream Data" + bcolors.ENDC)
    # getStreamData(streamName,verbose)



logChainInit()