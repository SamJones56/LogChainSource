import os
import subprocess

# REPLACE with your chain name
BRIDGE_CHAIN_NAME = "logChain"
# If you used custom params for a join in node1, replicate them here
# Or if you just want to run 'multichaind MyChain -daemon' you can do that

try:
    # Start the bridging node
    subprocess.run(["multichaind", BRIDGE_CHAIN_NAME, "-daemon"], check=True)

    # (Optional) Subscribe to certain streams. Example:
    # subprocess.run(["multichain-cli", BRIDGE_CHAIN_NAME, "subscribe", "my_stream"], check=True)

    print("Bridge node started successfully.")

except Exception as e:
    print(f"Error starting bridge node: {e}")
    exit(1)