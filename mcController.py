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
            break
        time.sleep(1)
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage()+'\n')

# Take wallet address as input and connect to genesis node
def connectToChain(walletAddress):
    permissions = "connect,send,receive"
    txid = mc.grant(walletAddress, permissions)
    connect(txid)


# Create a stream -> give name + restrictions in JSON format
def createStream(streamName, streamRestrictions):
    txid=mc.create('stream', streamName, streamRestrictions)
    connect(txid)


# Subscribe to existing stream
def subStream(streamName):
    try:
        mc.subscribe(streamName)
        print(f"Successfully subscribed to stream: {streamName}")
    except Exception as e:
        print(f"Failed to subscribe stream: {streamName}")
    

# Grant stream permissions
def grantStream(walletAddress, streamName):
    txid = mc.grant(walletAddress, streamName)
    connect(txid)