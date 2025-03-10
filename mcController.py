from multichain import MultiChainClient
import subprocess
import json

rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'         

# Setup client
mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

# Take wallet address as input and connect to genesis node
def connectToChain(address):
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
    # type = "type=" + name
    # try:
    #     response = mc.create("type=stream", name, restrictions)
    #     print("Stream status: ", response)
    # except Exception as e:
    #     print("Error granting permissions:", str(e))
    txid=mc.create('stream', name, restrictions)

    if mc.success():
        print("Stream: ", name, " successful")
        pass # operation was successful

    else: # operation failed
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage()+'\n')
