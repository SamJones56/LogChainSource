from multichain import MultiChainClient
import time


rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'         

# Setup client
mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

def connect(txid):
    for i in range(120):
        mc.getrawtransaction(txid)
        if mc.success():
            print("Successful: ", txid)
            return True
        time.sleep(1)
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage()+'\n')

# Take wallet address as input and connect to genesis node
def connectToChain(walletAddress):
    permissions = "connect,send,receive"
    txid = mc.grant(walletAddress, permissions)
    return(connect(txid))


# Create a stream -> give name + restrictions in JSON format
def createStream(streamName, streamRestrictions):
    txid=mc.create('stream', streamName, streamRestrictions)
    connect(txid)


# Subscribe to existing stream
def subStream(streamName):
    txid=mc.subscribe(streamName)
    return(connect(txid))

# Grant stream permissions
def grantStream(walletAddress, streamName, permissionType):
    streamPerms = (streamName + "." + permissionType)
    txid = mc.grant(walletAddress, streamPerms)
    return(connect(txid))