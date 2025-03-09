from multichain import MultiChainClient
import multichain

rpchost='127.18.0.2' # change if multichaind is not running locally
rpcport=7011 # usually default-rpc-port in blockchain parameters
rpcuser='genesis' # see multichain.conf in blockchain directory
rpcpassword='logChain' # see multichain.conf in blockchain directory

mc=MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

txmid=mc.publish('strream1', 'key1', {'json' : {'name' : 'john', 'age' : 30}})

if mc.success():
    pass

else:
    print('error')