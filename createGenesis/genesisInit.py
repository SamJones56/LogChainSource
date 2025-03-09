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

# multihain Generation
def genChain():

     # Generate logChain with correct params
     print(bcolors.OKGREEN + "multichain-util create logChain -default-network-port=7010 -default-rpc-port=7011" + bcolors.OKGREEN)
     cmd = ["multichain-util", "create", "logChain", "-default-network-port=7010", "-default-rpc-port=7011"]
     subprocess.run(cmd)

     # Editing the logChain config file
     # Path to conf file
     confPath = "/root/.multichain/logChain/multichain.conf"
     # Custom values
     rpcuser = "genesis"
     rpcpassword = "logChain"
     rpcallowip = "rpcallowip=172.16.0.0/16"

     # Wait for file to be created
     for i in range(60):
          if os.path.exists(confPath):
               print(bcolors.OKGREEN + "------------------ PATH FOUND -------------------"+ bcolors.OKGREEN) 
               break
          time.sleep(1)

     # Read and edit file
     lines = []
     with open(confPath, "r") as f:
          for line in f:
               if line.startswith("rpcuser="):
                    lines.append(f"rpcuser={rpcuser}\n")
               if line.startswith("rpcpassword="):
                    lines.append(f"rpcpassword={rpcpassword}\n")
               lines.append(rpcallowip)

     # Write to file
     with open(confPath, "w") as f:    
          print(bcolors.OKGREEN + f"writing {confPath} : rpcuser={rpcuser}, pcpassword={rpcpassword}, {rpcallowip}" + bcolors.OKGREEN)
          f.writelines(lines)

     time.sleep(5)

     # Starting the daemon
     print(bcolors.OKGREEN + "multichaind logChain -daemon" + bcolors.OKGREEN)
     cmd = ["multichaind", "logChain", "-daemon"]
     subprocess.run(cmd)

genChain()