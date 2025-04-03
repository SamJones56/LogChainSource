import subprocess
import re
import time
from colours import bcolors
from mcController import connectToChain, grantStream ,getPubKey
from cryptoUtils import genSudoFile

keyFile = "keys/kPk.key"
streamName = "pubkeys"
streamKey = "genesis"

# Connect and grant permissions on an existing chain
def connectAndPerm(streamName, walletAddress, permission):
    time.sleep(5)
    # Set permissions
    print(bcolors.OKGREEN + f"Subscribing to {streamName}"  + bcolors.ENDC)
    # Subscribe to stream
    subprocess.run(["multichain-cli","logChain","subscribe", f"{streamName}"])
    # Request permissions on stream
    print(bcolors.OKCYAN + f"Granting on {streamName}" + bcolors.ENDC)
    permissions = streamName + permission
    grantStream(walletAddress ,permissions)
    time.sleep(5)
    
def savePk():
    time.sleep(5)
    print(bcolors.OKCYAN + f"Pulling Genesis Public Kyber Key from {streamName}" + bcolors.ENDC)
    data = getPubKey(streamName,streamKey)
    print(bcolors.OKGREEN + f"Saving Kyber Puiblic Key to {keyFile}" + bcolors.ENDC)
    with open(keyFile,"wb") as f:
        f.write(data)

def logChainInit():
    # Connect to logChain
    print(bcolors.OKGREEN + "multichaind logChain@172.18.0.2:7010" + bcolors.ENDC)
    cmd = ["multichaind", "logChain@172.18.0.2:7010"]
    # Get the address string after connecting
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Extract address from output string
    # https://www.w3schools.com/python/python_regex.asp
    walletAddress = re.search(r"multichain-cli logChain grant (\w+) connect", result.stdout)
    walletAddress = walletAddress.group(1)
    # Get wallet address
    if walletAddress:
        print(bcolors.OKGREEN + f"ADDRESS FOUND: {walletAddress} " + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "ADDRESS NOT FOUND" + bcolors.ENDC)
    # Connect to logChain
    print(bcolors.OKCYAN + "Connecting to Chain " + bcolors.ENDC)
    connectToChain(walletAddress)

    # Start daemon
    print(bcolors.OKGREEN + "multichaind logChain -daemon" + bcolors.ENDC)
    subprocess.run(["multichaind", "logChain", "-daemon"])
    
    # Connect and grant permissions on an existing chain
    connectAndPerm("pubkeys", walletAddress, ".write,read")
    connectAndPerm("data", walletAddress, ".read")

    # Generate public key file
    genSudoFile(keyFile)
    # Save genesis public key
    savePk()
    print(bcolors.OKGREEN + "----- NODE DONE ----- " + bcolors.ENDC)

logChainInit()