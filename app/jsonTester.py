from multichain import MultiChainClient
import time

rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'  

# Setup client
mc = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

if mc.success():
    pass
else:
    print('Error code: '+str(mc.errorcode())+'\n')
    print('Error message: '+mc.errormessage() +'\n')