import subprocess, json

# https://stackoverflow.com/questions/287871/how-do-i-print-colored-text-to-the-terminal
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

#### Create the docker network ####
# Define as a swarm node
def swarmCreate():
    cmd = ["docker","swarm","init"]
    return cmd
# Delete current network if exists
def netDelete():
    print(bcolors.WARNING + "Removing old netwokrs" + bcolors.WARNING)
    cmd = ["docker", "network", "rm", "Multichain-Network"]
    return cmd

# Create new network
def netCreate():
    print(bcolors.OKBLUE + "Name: Multichain-network, Subnet: 192.168.1.0/24" + bcolors.ENDC)
    cmd = ["docker", "network", "create", "-d", "overlay", "--attachable", "--subnet","192.168.1.0/24","Multichain-Network"]
    return cmd

# Network Generation Commands
netGen = [swarmCreate, netDelete, netCreate]

#### Docker Image Setup ####
# Delete Old Image
def imageDelete():
    print(bcolors.WARNING + "Removing old images" + bcolors.WARNING)
    cmd = ["docker", "rmi", "multichain_image", "."]
    return cmd
 
# Build New Docker Image
def genesisCreate():
    print(bcolors.OKBLUE + "Creating image" + bcolors.ENDC)
    cmd = ["docker", "build", "-f", "genesisMain\Docker", "-t", "multichain_genesis_image", "."]
    return cmd

# Build New Docker Image
def nodeCreate():
    print(bcolors.OKBLUE + "Creating image" + bcolors.ENDC)
    cmd = ["docker", "build", "-f", "node1Main\Docker", "-t", "multichain_node_image", "."]
    return cmd

# Image Generation Commands
imageGen = [imageDelete, genesisCreate, nodeCreate]

#### Docker Container Setup ####
# host count for ips
hosts = 0

# Delete old containers
def contClear():
    print(bcolors.WARNING + "Removing old containers" + bcolors.WARNING)
    cmd = ["docker", "rm", "$(docker ps -q)"]
    return cmd

# Create Genesis node
def genesisCreate():
    global hosts
    hosts += 1
    print(bcolors.OKBLUE + "Creating Genesis: IP: 192.168.1.2, Ports - 6000,6001,6002" + bcolors.ENDC)
    with open("cont.json", "r") as file:
        data = json.load(file)
        return data.get("genesis", [])

# Create Node1
def node1Create():
    global hosts
    hosts += 1
    print(bcolors.OKBLUE + "Creating Node1: IP: 192.168.1.3 Ports - 6010,6011,6012" + bcolors.ENDC)
    with open("cont.json", "r") as file:
        data = json.load(file)
        return data.get("node1", [])


# Container Generation Commands
contGen = [contClear, genesisCreate, node1Create]


commands = [netGen, imageGen, contGen]

# Run Commands
for cmd_group in commands:
    for cmd in cmd_group:
        print(bcolors.OKGREEN + f"Running {cmd.__name__}..." + bcolors.ENDC)
        subprocess.run(cmd())