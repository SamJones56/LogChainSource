from multichain import MultiChainClient
import time
import functools

rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'         

# Setup client
mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

def connect(mc):
    for i in range(60):
        if mc.success():
            print("Successful")
            break # operation was successful
        time.sleep(1)
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage()+'\n')

# Take wallet address as input and connect to genesis node
def connectToChain(walletAddress):
    permissions = "connect,send,receive"
    connect(mc.grant(walletAddress, permissions))
    # print(mc.grant(walletAddress, permissions))
    # if mc.success():
    #     print("Chain: ", walletAddress, " successful")
    #     pass # operation was successful
    # else:
    #     print('Error code: '+str(mc.errorcode())+'\n')
    #     print('Error message: '+mc.errormessage()+'\n')


# Create a stream -> give name + restrictions in JSON format
def createStream(streamName, streamRestrictions):
    connect(mc.create('stream', streamName, streamRestrictions))
    # print(mc.create('stream', streamName, streamRestrictions))
    # for i in range(120):
    #     if mc.success():
    #         print("Stream: ", streamName, " successful")
    #         break # operation was successful
    #     time.sleep(1)
    #     print('Error code: '+str(mc.errorcode())+'\n')
    #     print('Error message: '+mc.errormessage()+'\n')


# Subscribe to existing stream
def subStream(streamName):
    txid=mc.subscribe(streamName)