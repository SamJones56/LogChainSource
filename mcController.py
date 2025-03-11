from multichain import MultiChainClient
import time
import functools

rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'         

# Setup client
mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

def errorHandle(f):
    @functools.wraps(f)
    def inner(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as ex:
            print(ex)
    return inner



# Take wallet address as input and connect to genesis node
@errorHandle
def connectToChain(walletAddress):
    permissions = "connect,send,receive"
    raise Exception(mc.grant(walletAddress, permissions))
    # if mc.success():
    #     print("Chain: ", walletAddress, " successful")
    #     pass # operation was successful
    # else:
    #     print('Error code: '+str(mc.errorcode())+'\n')
    #     print('Error message: '+mc.errormessage()+'\n')


# Create a stream -> give name + restrictions in JSON format
def createStream(streamName, streamRestrictions):
    txid=mc.create('stream', streamName, streamRestrictions)
    for i in range(120):
        if mc.success():
            print("Stream: ", streamName, " successful")
            break # operation was successful
        time.sleep(1)
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage()+'\n')


# Subscribe to existing stream
def subStream(streamName):
    txid=mc.subscribe(streamName)



# def connect(mc):
    # for i in range(120):
    #     if mc.success():
    #         print("Success")
    #         break
    #     time.sleep(1)
    #     print('Error code: '+str(mc.errorcode())+'\n')
    #     print('Error message: '+mc.errormessage()+'\n')