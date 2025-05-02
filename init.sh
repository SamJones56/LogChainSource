# Delete old volumes
echo "-------- Removing old volumes --------"
rm -rf ../multichain/genesis_data/
rm -rf ../multichain/node1_data/
rm -rf ../multichain/node2_data/
rm -rf ../multichain/kali/

echo "-------- Creating directories for volumes --------"
mkdir ../multichain/genesis_data/
mkdir ../multichain/node1_data/
mkdir ../multichain/node2_data/
mkdir ../../multichain/kali/

# Build docker
echo "---------- Down Docker ----------"
docker compose down 
echo "---------- Building Docker ----------"
# uncomment -d to run detached
docker compose up --build #-d