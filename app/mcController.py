from multichain import MultiChainClient
import time
from colours import bcolors

# https://www.multichain.com/developers/json-rpc-api/
rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'         
# Setup client
mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

# Take wallet address as input and connect to genesis node
def connectToChain(walletAddress):
    permissions = "connect,send,receive"
    txid = mc.grant(walletAddress, permissions)
    # connect(txid)
    for i in range(60):
        mc.getrawtransaction(txid)
        if mc.success():
            print(bcolors.OKGREEN + f"Successfully Connected: {walletAddress} with Permissions {permissions}" + bcolors.ENDC)
            break
        time.sleep(1)
        print(bcolors.FAIL + 'Error code: '+str(mc.errorcode())+ bcolors.ENDC +'\n')
        print(bcolors.FAIL + 'Error message: '+mc.errormessage()+ bcolors.ENDC +'\n')

# Create a stream -> give name + restrictions in JSON format
def createStream(streamName, streamRestrictions):
    txid=mc.create('stream', streamName, streamRestrictions)
    # connect(txid)
    for i in range(60):
        mc.getrawtransaction(txid)
        if mc.success():
            print(bcolors.OKGREEN + f"Successfully created stream: {streamName}" + bcolors.ENDC)
            break
        time.sleep(1)
        print(bcolors.FAIL + 'Error code: '+str(mc.errorcode())+ bcolors.ENDC +'\n')
        print(bcolors.FAIL + 'Error message: '+mc.errormessage()+ bcolors.ENDC +'\n')


# Subscribe to existing stream
def subStream(chainName, streamName):
    print(bcolors.OKCYAN + f"Subscribed to stream: {streamName} on {chainName}" +bcolors.ENDC)
    mc.subscribe(streamName)

# Grant stream permissions
def grantStream(walletAddress, permissions):
    txid = mc.grant(walletAddress, permissions)
    # connect(txid)
    if mc.success():
        print(bcolors.OKGREEN +f"Success. Permissions {permissions} Granted. {txid}" + bcolors.ENDC)
    else:
        print(bcolors.FAIL +'Error code: ' + str(mc.errorcode()) + bcolors.ENDC + '\n')
        print(bcolors.FAIL +'Error message: ' + mc.errormessage() + bcolors.ENDC + '\n')

# Add items to stream w/ option
def addToStream(streamName, key, data):
    txid = mc.publish(streamName, key, data)
    if mc.success():
        print(bcolors.OKGREEN + f"Successfully added to {streamName}" + bcolors.ENDC)
        return txid 
    else:
        print(bcolors.FAIL +'Error code: ' + str(mc.errorcode()) + bcolors.ENDC + '\n')
        print(bcolors.FAIL +'Error message: ' + mc.errormessage() + bcolors.ENDC + '\n')

# Add items to stream
def addToStreamOptions(streamName, key, data, options=""):
    txid = mc.publish(streamName, key, data, options)
    if mc.success():
        print(bcolors.OKGREEN + f"Successfully added to {streamName}" + bcolors.ENDC)
        return txid 
    else:
        print(bcolors.FAIL +'Error code: ' + str(mc.errorcode()) + bcolors.ENDC + '\n')
        print(bcolors.FAIL +'Error message: ' + mc.errormessage() + bcolors.ENDC + '\n')

# Get stream items
def getStreamData(streamName, verbose):
    response = mc.liststreamitems(streamName,verbose, 9999)
    if mc.success():
        return(response)
    else:
        print(bcolors.FAIL +'Error code: ' + str(mc.errorcode())+ bcolors.ENDC + '\n')
        print(bcolors.FAIL +'Error message: ' + mc.errormessage() + bcolors.ENDC + '\n')

# Get address
def getAddress():
    address = mc.getaddresses()
    if mc.success():
        pass
    else:
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage() +'\n')
    return address

# Publish from
def publishFrom(fromAddress, stream, key, data):
    txid = mc.publishfrom(fromAddress, stream, key, data)
    if mc.success():
        pass
    else:
        print('Error code: '+str(mc.errorcode())+'\n')
    return txid

# list items
def listPublisherItems(stream, address, verbose, count):
    txid = mc.liststreampublisheritems(stream, address, verbose, count)
    if mc.success():
        pass
    else:
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage() +'\n')
    return txid

# List the stream items
def getPubKey(stream,key):
    txid = mc.liststreamkeyitems(stream, key)
    if mc.success():
        print(bcolors.OKGREEN + "Data Pulled" + bcolors.ENDC)
        pubkeyH = txid[0]["data"]
        return bytes.fromhex(pubkeyH)
    else:
        print('Error code: '+str(mc.errorcode())+'\n')
        print('Error message: '+mc.errormessage() +'\n')