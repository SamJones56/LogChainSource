import subprocess
import time
import os
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

def chainPerms():
    connectToChain()

def logChainInit():
    print(bcolors.OKGREEN + "multichaind logChain@172.18.0.2:7010 -daemon" + bcolors.ENDC)
    cmd = ["multichaind", "logChain@172.18.0.2:7010", "-daemon"]
    subprocess.run(cmd)

    # Path for logChain
    confPath = "/root/.multichain/logChain/multichain.conf"
    # Wait for multichain connection
    for i in range(120):
        if os.path.exists(confPath):
            print(bcolors.OKGREEN + "------------------ PATH FOUND -------------------"+ bcolors.ENDC) 
            break
        time.sleep(1)
    # Gather perms on the chain
    chainPerms() 
    

logChainInit()