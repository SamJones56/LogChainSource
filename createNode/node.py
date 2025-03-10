import subprocess
import time
import os
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

def chainPerms(address):
    connectToChain(address)

def logChainInit():
    print(bcolors.OKGREEN + "multichaind logChain@172.18.0.2:7010 -daemon" + bcolors.ENDC)
    cmd = ["multichaind", "logChain@172.18.0.2:7010", "-daemon"]
    # Get the address string
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Extract address from output string

    address = re.search(r"multichain-cli logChain grant (\w+) connect", result.stdout)

    address = address.group(1)
    print(address)
    # Path for logChain
    confPath = "/root/.multichain/logChain/multichain.conf"


    # Wait for multichain connection
    for i in range(120):
        if address:
            print(bcolors.OKGREEN + "------------------ ADDRESS FOUND -------------------"+ bcolors.ENDC) 
            break
        time.sleep(1)
    # Gather perms on the chain
    chainPerms(address) 
    

logChainInit()