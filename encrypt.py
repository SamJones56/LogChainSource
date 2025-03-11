import subprocess
import os
from mcController import publishFrom, listPublisherItems

def mkdir(name):
    os.makedirs(name)

# genesis
def createKey(walletAddress, stream):
    # Create directory for storage
    mkdir("stream-privkeys")
    path = f"stream-privkeys/{walletAddress}.pem"
    # Create keys
    subprocess.run(["openssl", "genpkey", "-algorithm", "RSA", "-out", path])
    # Convert to hex
    pubKeyHex = subprocess.run(["openssl", "rsa", "-pubout", "-in", path, "|", "xxd", "-p", "-c", "9999"], capture_output=True)
    # Publish to chain
    txid = publishFrom(walletAddress, stream, pubKeyHex)
    return txid

# node
def createCt(walletAddress, stream, data):
    # Generate random password
    password = subprocess.run(["openssl","rand","-base64","48"], capture_output=True)
    # Create ciphertext
    ct = subprocess.run(["openssl","enc","-aes-256-cbc","-in",{data},"-pass", {password}, "|", "xxd", "-p", "-c", "99999"],capture_output=True)
    # Publish to chain
    txid = publishFrom(walletAddress, stream, ct)
    # Create password directory
    mkdir("stream-passwords")
    path = f"stream-privkeys/{txid}.txt"
    # save password to dir
    subprocess.run(["echo",password,">",path])
    return txid

# search for pub key (node searches foe genesis)
def getPubKey(walletAddress):
    stream = "pubkeys"
    txid = listPublisherItems(stream, )