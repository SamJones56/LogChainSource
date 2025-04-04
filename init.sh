# Delete old volumes
echo "-------- Removing old volumes --------"
rm -rf ../multichain/genesis_data/
rm -rf ../multichain/node1_data/
rm -rf ../multichain/node2_data/

echo "-------- Creating directories for volumes --------"
mkdir ../multichain/genesis_data/
mkdir ../multichain/node1_data/
mkdir ../multichain/node2_data/

# Build docker
echo "---------- Down Docker ----------"
docker compose down 
echo "---------- Building Docker ----------"
# uncomment -d to run detached
docker compose up --build #-d