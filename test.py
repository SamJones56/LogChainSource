from multichain import MultiChainClient

rpchost='127.0.0.1' # change if multichaind is not running locally
rpcport=7011 # usually default-rpc-port in blockchain parameters
rpcuser='multichainrpc' # see multichain.conf in blockchain directory
rpcpassword='5wGmipV7CrQSGkRPPN1fCu8xxSFKfymQmKX89CtwVvES' # see multichain.conf in blockchain directory

mc=MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)