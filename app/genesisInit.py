import subprocess
import time
import os
from colours import bcolors
from mcController import createStream, addToStream, subStream
from cryptoUtils import kyberGenKeys, readFromFile, genSudoFile
from userInterface import getPassword

# multihain Generation
def genChain():
     # Generate logChain with correct params
     print(bcolors.OKCYAN + "Creating Multichain Blockchain" + bcolors.ENDC)
     print(bcolors.OKGREEN + "multichain-util create logChain -default-network-port=7010 -default-rpc-port=7011" + bcolors.ENDC)
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
               print(bcolors.OKGREEN + "MultiChain Created"+ bcolors.ENDC) 
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
          print(bcolors.OKCYAN + f"Writing to {confPath}: rpcuser={rpcuser}, rpcpassword={rpcpassword}, {rpcallowip}" + bcolors.ENDC)
          f.writelines(lines)

     # Writing time
     time.sleep(5)

     # Starting the daemon
     print(bcolors.OKCYAN + "Initialising MultiChain" + bcolors.ENDC)
     print(bcolors.OKGREEN + "multichaind logChain -daemon" + bcolors.ENDC)
     cmd = ["multichaind", "logChain", "-daemon"]
     subprocess.run(cmd)
     time.sleep(3)
     # Create the streams
     # Key stream
     restrictions = {"restrict":"write"}
     streamName = "pubkeys"
     chainName = "logChain"
     print(bcolors.OKCYAN + "Create stream:" + streamName + bcolors.ENDC)
     createStream(streamName, restrictions)
     time.sleep(2)
     subStream(chainName, streamName)
     # Data stream
     restrictions = {"restrict":"write"}
     streamName = "data"
     print(bcolors.OKCYAN + "Create stream: " + streamName + bcolors.ENDC)
     createStream(streamName, restrictions)
     time.sleep(2)
     subStream(chainName, streamName)

     # Get password
     password = getPassword(bcolors.WARNING + "Enter Password for Encryption: " + bcolors.ENDC, False)

     # Generate key files
     print(bcolors.OKCYAN + "Generating Restricted Files" + streamName + bcolors.ENDC)
     genSudoFile("keys/kPk.key")
     genSudoFile("keys/kSk.key")
     # Generate kyber
     print(bcolors.OKCYAN + "Generating kyber keys" + bcolors.ENDC)
     kyberGenKeys(password)
     # Get the public key
     kpk = readFromFile("keys/kPk.key")
     # Post the pk to the pubkeys stream
     streamName = "pubkeys"
     print(bcolors.OKCYAN + "Adding public kypher key to stream " + bcolors.ENDC)
     addToStream(streamName, "genesis", kpk.hex())
     # Print when Done
     print(bcolors.OKGREEN + "----- GENESIS DONE ----- " + bcolors.ENDC)

genChain()