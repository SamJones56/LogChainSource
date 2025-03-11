import subprocess
import re
from mcController import connectToChain, subStream

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
    
    cmd = ["multichaind", "logChain@172.18.0.2:7010"]
    # subprocess.run(cmd)
    # Get the address string after connecting
    print(bcolors.OKCYAN + "multichaind logChain@172.18.0.2:7010" + bcolors.ENDC)
    result = subprocess.run(cmd, capture_output=True, text=True)
    # Extract address from output string
    # https://www.w3schools.com/python/python_regex.asp
    address = re.search(r"multichain-cli logChain grant (\w+) connect", result.stdout)
    address = address.group(1)

    print("getting address****")
    if address:
        print(bcolors.OKCYAN + f"ADDRESS FOUND: {address} " + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "ADDRESS NOT FOUND" + bcolors.ENDC)

    print("connecting to chain****")
    connectToChain(address)
    subprocess.run(["multichaind", "logChain", "-daemon"])
    # Get connect,send,receive from chain
    # if(connectToChain(address)):
    #     print(bcolors.OKCYAN + "multichaind logChain -daemon" + bcolors.ENDC)
    #     subprocess.run(["multichaind", "logChain", "-daemon"])
    # else:
    #     print(bcolors.FAIL + "FAIL Chain Connection" + bcolors.ENDC)
    
    print("Subbing to stream****")
    if(subStream("mainStream")):
        print(bcolors.OKCYAN + "Subscribed to mainStream" + bcolors.ENDC)
    else:
        print(bcolors.FAIL + "FAIL Stream Connection" + bcolors.ENDC)
    
    

logChainInit()