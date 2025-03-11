from multichain import MultiChainClient
import time

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

rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'         

# Setup client
mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

def connect(txid):
    for i in range(60):
        mc.getrawtransaction(txid)
        if mc.success():
            print(bcolors.OKGREEN + "Successful: ", txid + bcolors.ENDC)
            break
        time.sleep(1)
        print(bcolors.FAIL + 'Error code: '+str(mc.errorcode())+ bcolors.ENDC +'\n')
        print(bcolors.FAIL + 'Error message: '+mc.errormessage()+ bcolors.ENDC +'\n')

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
        print(bcolors.OKGREEN + f"Successfully subscribed to stream: {streamName}" + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + f"Failed to subscribe stream: {streamName}" + bcolors.ENDC)
    

# Grant stream permissions
def grantStream(walletAddress, streamName):
    permissions="write"
    txid = mc.grant(walletAddress, f"stream:{streamName}", permissions)
    connect(txid)