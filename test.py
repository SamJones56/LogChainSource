from multichain import MultiChainClient
import multichain

rpchost='127.18.0.2' # change if multichaind is not running locally
rpcport=7011 # usually default-rpc-port in blockchain parameters
rpcuser='genesis' # see multichain.conf in blockchain directory
rpcpassword='logChain' # see multichain.conf in blockchain directory

mc=MultiChainClient(rpchost, rpcport, rpcuser, rpcpassword)

address = "root/.multichain/logChain/wallet.dat"
walletAddr = ""
with open(address, "r") as f:
    for line in f:
        if line.startswith("Minimal blockchain parameter set is created, default address:"):
            walletAddr = line.split(":")[-1].strip()
            print("--------- WALLET ADDR ---------")
            print(walletAddr)
            break

# txid=mc.grant()
#curl -v --fail --user genesis:logChain 
# --data-binary '{ "method" : "grant", "params" : ["19DsJCDPFzMLnG66mMm94sPtLzGNPDoD77NHKx","connect,send,receive"], "id":"1", "jsonrpc":"2.0"}' 
# -H 'content-type: text/plain;' http://172.18.0.2:7011 