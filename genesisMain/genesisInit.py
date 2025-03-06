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

# multihain Generation ~ timer to wait for initialing daemon
def genChain():
     print(bcolors.OKGREEN + "Generating MultiChain" + bcolors.OKGREEN)
     cmd = ["multichain-util", "create", "logChain", "-default-network-port=6010", "-default-rpc-port=6011"]
     time.sleep(15)
     subprocess.run(cmd())

# multichain Daemon
def demChain():
     print(bcolors.OKGREEN + "Init chain" + bcolors.OKGREEN)
     cmd = ["multichaind", "logChain", "-daemon"]
     subprocess.run(cmd())

genesisCmds=[genChain, demChain]

for cmd in genesisCmds:
    cmd()