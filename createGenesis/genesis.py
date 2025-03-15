import subprocess
import time
import os
from mcController import createStream, getAddress, subStream

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
     print(bcolors.OKGREEN + "multichain-util create logChain -default-network-port=7010 -default-rpc-port=7011" + bcolors.ENDC)
     cmd = "multichain-util create logChain -default-network-port=7010 -default-rpc-port=7011"
     subprocess.run(cmd, shell=True)

     # Editing the logChain config file
     # Path to conf file
     confPath = "/root/.multichain/logChain/multichain.conf"
     # Custom values
     rpcuser = "genesis"
     rpcpassword = "logChain"
     rpcallowip = "rpcallowip=172.18.0.0/16"

     # Wait for log chain to be initialised
     for i in range(120):
          if os.path.exists(confPath):
               print(bcolors.OKGREEN + "------------------ PATH FOUND -------------------"+ bcolors.ENDC) 
               break
          time.sleep(1)

     # Read and edit the config file
     # https://www.w3schools.com/python/python_ref_list.asp
     lines = []
     with open(confPath, "r") as f:
          for line in f:
               if line.startswith("rpcuser="):
                    lines.append(f"rpcuser={rpcuser}\n")
               if line.startswith("rpcpassword="):
                    lines.append(f"rpcpassword={rpcpassword}\n")
     lines.append(f"{rpcallowip}\n")

     # Write to file
     with open(confPath, "w") as f:    
          print(bcolors.OKGREEN + f"writing {confPath} : rpcuser={rpcuser}, rpcpassword={rpcpassword}, {rpcallowip}" + bcolors.ENDC)
          f.writelines(lines)

     # Writing time
     time.sleep(5)

     # Starting the daemon
     print(bcolors.OKGREEN + "multichaind logChain -daemon" + bcolors.ENDC)
     cmd = ["multichaind", "logChain", "-daemon"]
     subprocess.run(cmd)

     time.sleep(20)
     # Create the streams
     # Key stream
     restrictions = {"restrict":"write"}
     name = "pubkeys"
     print(bcolors.OKGREEN + "Create stream:" + name + bcolors.ENDC)
     createStream(name, restrictions)

     # Data stream
     restrictions = {"restrict":"write"}
     name = "data"
     print(bcolors.OKGREEN + "Create stream:" + name + bcolors.ENDC)
     createStream(name, restrictions)


     # #### Setting up private chains ####
     # # Get address
     # walletAddress = getAddress()
     # # Create pubkeys(store public keys), items(store data), access stream (control access)
     # print(bcolors.OKGREEN + "Create pubkeys, items, access streams" + bcolors.ENDC)
     # restrictions = {"restrict":"write"}
     # pubkeys = "pubkeys"
     # items = "items"
     # access = "access"
     # createStream(pubkeys, restrictions)
     # createStream(items, restrictions)
     # createStream(access, restrictions)

     # streamName="pubkeys,items,access"
     # chainName="logChain"
     # subStream(chainName,streamName)
     # time.sleep(2)

genChain()