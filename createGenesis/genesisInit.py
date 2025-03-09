import subprocess
import time
import os

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
     cmd = ["multichain-util", "create", "logChain", "-default-network-port=7010", "-default-rpc-port=7011"]
     subprocess.run(cmd)


     # Path to conf file
     confPath = "/root/.multichain/logChain/multichain.conf"
     # Custom values
     rpcuser = "genesis"
     rpcpassword = "logChain"
     rpcallowip = "rpcallowip=172.16.0.0/16"

     # Wait for file to be created
     for i in range(60):
          if os.path.exists(confPath):
               print("------------------ PATH FOUND -------------------")
               break
          time.sleep(1)

     # Edit file
     lines = []
     with open(confPath, "r+") as f:
          for line in f:
               if line.startswith("rpcuser="):
                    lines.append(f"rpcuser={rpcuser}\n")
               if line.startswith("rpcpassword="):
                    lines.append(f"rpcpassword={rpcpassword}\n")
               lines.append(rpcallowip)
          f.writelines(lines)


     # cmd = "echo 'rpcallowip=172.16.0.0/16' >> /root/.multichain/logChain/multichain.conf"
     # subprocess.run(cmd, shell=True)


     time.sleep(5)

# multichain Daemon
def demChain():
     print(bcolors.OKGREEN + "Init chain" + bcolors.OKGREEN)
     cmd = ["multichaind", "logChain", "-daemon"]
     subprocess.run(cmd)

genesisCmds=[genChain, demChain]

for cmd in genesisCmds:
    cmd()