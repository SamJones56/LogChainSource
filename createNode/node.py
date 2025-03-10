import subprocess
import re
from mcController import connectToChain

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

# Get perms on chain
def chainPerms(address):
    connectToChain(address)

def logChainInit():
    # Connect to logChain
    print(bcolors.OKGREEN + "multichaind logChain@172.18.0.2:7010 -daemon" + bcolors.ENDC)
    cmd = ["multichaind", "logChain@172.18.0.2:7010"]
    subprocess.run(cmd)
    # Get the address string after connecting
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Extract address from output string
    # https://www.w3schools.com/python/python_regex.asp
    address = re.search(r"multichain-cli logChain grant (\w+) connect", result.stdout)
    address = address.group(1)

    if address:
        print(bcolors.OKGREEN + f"ADDRESS FOUND: {address} " + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "ADDRESS NOT FOUND" + bcolors.ENDC)

    # Get connect,send,receive from chain
    chainPerms(address) 
    

logChainInit()