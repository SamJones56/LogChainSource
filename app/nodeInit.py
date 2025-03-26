import subprocess
import re
import time
from colours import bcolors
from mcController import connectToChain, subStream, grantStream ,getPubKey

# Connect and grant permissions on an existing chain
def connectAndPerm(chainName, streamName, walletAddress):
    time.sleep(5)
    # Set permissions
    print(bcolors.WARNING + "Subscribing to " + streamName + bcolors.ENDC)
    # Subscribe to stream
    subprocess.run(["multichain-cli","logChain","subscribe", f"{streamName}"])
    
    # Request permissions on stream
    print(bcolors.WARNING + "Granting on " + streamName + bcolors.ENDC)
    permissions = streamName + ".write,read"
    grantStream(walletAddress ,permissions)
    time.sleep(5)
    
    

def savePk():
    time.sleep(5)
    print(bcolors.WARNING + "Saving puiblic key " + bcolors.ENDC)
    pkFile="kPk.key"
    data = getPubKey("pubkeys","genesis")
    with open(pkFile,"wb") as f:
        f.write(data)

def logChainInit():
    # Connect to logChain
    print(bcolors.OKCYAN + "multichaind logChain@172.18.0.2:7010" + bcolors.ENDC)
    cmd = ["multichaind", "logChain@172.18.0.2:7010"]
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
    # Connect to logChain
    print(bcolors.WARNING + "Connecting to Chain" + bcolors.ENDC)
    connectToChain(walletAddress)

    # Start daemon
    print(bcolors.OKCYAN + "multichaind logChain -daemon" + bcolors.ENDC)
    subprocess.run(["multichaind", "logChain", "-daemon"])
    
    # time.sleep(10)
    # Connect and grant permissions on an existing chain
    connectAndPerm("logChain", "pubkeys", walletAddress)
    connectAndPerm("logChain", "data", walletAddress)

    # Save genesis public key
    savePk()
    print(bcolors.OKGREEN + "----- NODE DONE ----- " + bcolors.ENDC)


logChainInit()