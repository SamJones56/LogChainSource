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

# Remove local directories
def remGenLocal():
    cmd=["rm", "-rf", "genesis"]
    return cmd

def remNodeLocal():
    cmd=["rm", "-rf", "node1"]
    return cmd

remLocal = [remGenLocal, remNodeLocal]

#### Create the docker network ####
# Leave swarm node
def swarmLeave():
    cmd=["docker", "swarm", "leave", "--force"]
    return cmd

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
netGen = [swarmLeave, swarmCreate, netDelete, netCreate]

#### Docker Image Setup ####
# Delete Old Image
def genDelete():
    print(bcolors.WARNING + "Removing old images" + bcolors.WARNING)
    cmd = ["docker", "rmi", "multichain_genesis_image", "."]
    return cmd

def nodeDelete():
    print(bcolors.WARNING + "Removing old images" + bcolors.WARNING)
    cmd = ["docker", "rmi", "multichain_node_image", "."]
    return cmd
 
# Build New Docker Image
def genesisCreate():
    print(bcolors.OKBLUE + "Creating image" + bcolors.ENDC)
    cmd = ["docker", "build", "-f", "./genesisMain/Docker", "-t", "multichain_genesis_image", "."]
    return cmd

# Build New Docker Image
def nodeCreate():
    print(bcolors.OKBLUE + "Creating image" + bcolors.ENDC)
    cmd = ["docker", "build", "-f", "./nodeMain/Docker", "-t", "multichain_node_image", "."]
    return cmd

# Image Generation Commands
imageGen = [genDelete, nodeDelete,genesisCreate, nodeCreate]

#### Docker Container Setup ####
# host count for ips
hosts = 0

# Delete old containers
def contClear():
    print(bcolors.WARNING + "Removing old containers" + bcolors.WARNING)
    running = subprocess.run(["docker", "ps", "-q"], capture_output=True, text=True)
    contId = running.stdout.strip().split('\n')
    for i in contId:
        cmd = ["docker", "rm", "-f", i]
        return cmd
    

# Create Genesis node
def genesisCreate():
    global hosts
    hosts += 1
    print(bcolors.OKBLUE + "Creating Genesis: IP: 192.168.1.2, Ports - 6010-6019" + bcolors.ENDC)
    with open("cont.json", "r") as file:
        data = json.load(file)
        return data.get("genesis", [])

# Create Node1
def node1Create():
    global hosts
    hosts += 1
    print(bcolors.OKBLUE + "Creating Node1: IP: 192.168.1.3 Ports - 6020-6029" + bcolors.ENDC)
    with open("cont.json", "r") as file:
        data = json.load(file)
        return data.get("node1", [])


# Container Generation Commands
contGen = [contClear, genesisCreate, node1Create]


commands = [remLocal ,netGen, imageGen, contGen]

# Run Commands
for cmd_group in commands:
    for cmd in cmd_group:
        print(bcolors.OKGREEN + f"Running {cmd.__name__}..." + bcolors.ENDC)
        subprocess.run(cmd())