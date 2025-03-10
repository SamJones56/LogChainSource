from multichain import MultiChainClient
import subprocess
import json

rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'         

# Setup client
# mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

# Take wallet address as input and connect to genesis node
def connectToChain(address):
    mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)
    permissions = "connect,send,receive"
    txid = mc.grant(address, permissions)
    if mc.success():
        print("Chain: ", address, " successful")
        pass # operation was successful
    else:
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage()+'\n')

# Create a stream -> give name + restrictions in JSON format
def createStream(name, restrictions):
    mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)
    txid=mc.create('stream', name, restrictions)

    if mc.success():
        print("Stream: ", name, " successful")
        pass # operation was successful

    else: # operation failed
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage()+'\n')
