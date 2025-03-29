import subprocess
import time
import os
from colours import bcolors
from mcController import createStream, addToStream, subStream
from app.cryptoUtils import genKeys
from utils import readFromFile

# multihain Generation
def genChain():
     # Generate logChain with correct params
     print(bcolors.OKGREEN + "multichain-util create logChain -default-network-port=7010 -default-rpc-port=7011" + bcolors.ENDC)
     # cmd = "multichain-util create logChain -default-network-port=7010 -default-rpc-port=7011"
     subprocess.run(["multichain-util", "create", "logChain", "-default-network-port=7010", "-default-rpc-port=7011"])

     # Editing the logChain config file
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
     streamName = "pubkeys"
     chainName = "logChain"
     print(bcolors.OKGREEN + "Create stream:" + streamName + bcolors.ENDC)
     createStream(streamName, restrictions)
     time.sleep(2)
     subStream(chainName, streamName)
     # Data stream
     restrictions = {"restrict":"write"}
     streamName = "data"
     print(bcolors.OKGREEN + "Create stream:" + streamName + bcolors.ENDC)
     createStream(streamName, restrictions)
     time.sleep(2)
     subStream(chainName, streamName)

     # Generate kyber
     print(bcolors.OKGREEN + "Generating kyber keys" + bcolors.ENDC)
     genKeys()
     # Get the public key
     kpk = readFromFile("kPk.key")
     # Post the pk to the pubkeys stream
     streamName = "pubkeys"
     print(bcolors.OKGREEN + "Adding public kypher key to stream " + bcolors.ENDC)
     addToStream(streamName, "genesis", kpk.hex())
     # Print when Done
     print(bcolors.OKGREEN + "----- GENESIS DONE ----- " + bcolors.ENDC)

genChain()