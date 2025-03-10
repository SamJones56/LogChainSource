from multichain import MultiChainClient
import subprocess
import json

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
        print("Grant status: " + response + ". Starting")
        subprocess.run(["multichaind", "logChain", "-daemon"])
    except Exception as e:
        print("Error granting permissions:", str(e))

# Create a stream -> give name + restrictions in JSON format
def createStream(name, restrictions):
    type = "stream"
    # https://www.w3schools.com/python/python_json.asp
    # restrictions = json.loads(restrictions)
    print(restrictions)
    try:
        response = client.create(type, name, restrictions)
        print("Stream status: ", response)
    except Exception as e:
        print("Error granting permissions:", str(e))