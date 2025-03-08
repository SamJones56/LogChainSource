import subprocess
import time

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

def demChain():
     time.sleep(20)
     print(bcolors.OKGREEN + "Init chain" + bcolors.OKGREEN)
     cmd = ["multichaind", "logChain@172.18.0.2:7010"]
     subprocess.run(cmd)

demChain()