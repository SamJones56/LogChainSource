import subprocess
import re
import time
from mcController import connectToChain, subStream, grantStream

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

    # Connect to mainStream
    streamName = "mainStream"
    print(bcolors.WARNING + "Subscribing to mainStream" + bcolors.ENDC)
    subStream(streamName)
    time.sleep(2)

    # Get permissions for mainStream
    print(bcolors.WARNING + "Granting on mainStream" + bcolors.ENDC)
    permissions = "mainStream.write"
    grantStream(walletAddress, permissions)

logChainInit()