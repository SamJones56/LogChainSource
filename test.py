from multichain import MultiChainClient

rpchost='127.18.0.2' # change if multichaind is not running locally
rpcport=7011 # usually default-rpc-port in blockchain parameters
rpcuser='genesis' # see multichain.conf in blockchain directory
rpcpassword='logChain' # see multichain.conf in blockchain directory

mc=MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

