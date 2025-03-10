from multichain import MultiChainClient
import subprocess

rpcuser = 'genesis'
rpcpassword = 'logChain'
rpchost = '172.18.0.2' 
rpcport = '7011'         

# Setup client
client = MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

# Take wallet address as input and connect to genesis node
def connectToChain(address):
    permissions = "connect,send,receive"
    try:
        response = client.grant(address, permissions)
        print("Grant successful: " + response + ". Starting")
        subprocess.cun("multichaind logChain -daemon")
    except Exception as e:
        print("Error granting permissions:", str(e))

