from multichain import MultiChainClient

rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'         

# Setup client
client = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

# Get blockchain info
info = client.getinfo()
print(info)