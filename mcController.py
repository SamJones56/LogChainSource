from multichain import MultiChainClient
import time
import subprocess

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

# def connect(txid):
#     for i in range(60):
#         mc.getrawtransaction(txid)
#         if mc.success():
#             print(bcolors.OKGREEN + "Successful: ", txid + bcolors.ENDC)
#             break
#         time.sleep(1)
#         print(bcolors.FAIL + 'Error code: '+str(mc.errorcode())+ bcolors.ENDC +'\n')
#         print(bcolors.FAIL + 'Error message: '+mc.errormessage()+ bcolors.ENDC +'\n')

# Take wallet address as input and connect to genesis node
def connectToChain(walletAddress):
    permissions = "connect,send,receive"
    txid = mc.grant(walletAddress, permissions)
    # connect(txid)
    for i in range(60):
        mc.getrawtransaction(txid)
        if mc.success():
            print(bcolors.OKGREEN + "Successfully granted: " + walletAddress + permissions + bcolors.ENDC)
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
            print(bcolors.OKGREEN + "Successfully created stream : ", streamName + bcolors.ENDC)
            break
        time.sleep(1)
        print(bcolors.FAIL + 'Error code: '+str(mc.errorcode())+ bcolors.ENDC +'\n')
        print(bcolors.FAIL + 'Error message: '+mc.errormessage()+ bcolors.ENDC +'\n')



# Subscribe to existing stream
def subStream(chainName, streamName):
    print(bcolors.OKGREEN + "Subscribed to stream:", streamName + " on: " + chainName +bcolors.ENDC)
    mc.subscribe(streamName)
    time.sleep(5)

# Grant stream permissions
def grantStream(walletAddress, permissions):
    txid = mc.grant(walletAddress, permissions)
    # connect(txid)
    if mc.success():
        print(bcolors.OKGREEN +"Success: " + txid + bcolors.ENDC)
        print(permissions)
    else:
        print(bcolors.FAIL +'Error code: ' + str(mc.errorcode()) + bcolors.ENDC + '\n')
        print(bcolors.FAIL +'Error message: ' + mc.errormessage() + bcolors.ENDC + '\n')

# Add items to stream
def addToStream(streamName, key, data):
    txid = mc.publish(streamName, key, data)
    if mc.success():
        print(bcolors.OKGREEN + "Successfully added to " + streamName + bcolors.ENDC)
        return txid 
    else:
        print(bcolors.FAIL +'Error code: ' + str(mc.errorcode()) + bcolors.ENDC + '\n')
        print(bcolors.FAIL +'Error message: ' + mc.errormessage() + bcolors.ENDC + '\n')

# Get stream items
def getStreamData(streamName, verbose):
    response = mc.liststreamitems(streamName,verbose)
    if mc.success():
        print(bcolors.OKGREEN + streamName + " Stream Items :" + bcolors.ENDC)
        print(response)
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