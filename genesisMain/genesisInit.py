import subprocess

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

# multihain Generation
def genChain():
     print(bcolors.OKGREEN + "Generating MultiChain" + bcolors.OKGREEN)
     cmd = ["multichain-util","create","logChain","-default-network-port=6010","default-rpc-port=6011"]
     return cmd

# multichain Daemon
def demChain():
     print(bcolors.OKGREEN + "Init chain" + bcolors.OKGREEN)
     cmd = ["multichaind", "logChain@192.168.1.2:6010"]
     return cmd

genesisCmds=[genChain, demChain]

# commands = [genesisCmds]

# # Run Commands
# for cmd_group in commands:
for cmd in genesisCmds:
    print(bcolors.OKGREEN + f"Running {cmd.__name__}..." + bcolors.ENDC)
    subprocess.run(cmd())