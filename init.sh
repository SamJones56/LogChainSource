
# Delete old volumes
echo "-------- Removing old volumes --------"
rm -rf ../multichain/genesis_data/
rm -rf ../multichain/node1_data/

echo "-------- Creating directories for volumes --------"
mkdir ../multichain/genesis_data/
mkdir ../multichain/node1_data/

# Build docker
echo "B---------- Down Docker ----------"
docker compose down 
echo "---------- Building Docker ----------"
docker compose up --build #-d

# # Wait for docker
# echo "waiting 60s for docker to build"
# sleep 60

# # Get debug.log info
# genesisContainer="multichain_genesis"
# node1Container="multichain_node1"

# echo "Pulling node1 address"
# node1addr=$(docker exec $node1Container grep "Minimal blockchain parameter set is created, default address: " /root/.multichain/logChain/debug.log | awk '{print $NF}')
# echo "Node1 address = $node1addr"

# # execute on genesis
# echo "executing connection on genesis"
# docker exec $genesisContainer multichain-cli logChain grant $node1addr connect,send,receive

# # execute on node1
# echo "starting node1 daemon"
# docker exec $node1Container multichaind logChain -daemon