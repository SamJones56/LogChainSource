# https://github.com/aabmets/quantcrypt
# https://github.com/aabmets/quantcrypt/wiki/Code-Examples
from colours import bcolors
from Crypto.Cipher import AES
from quantcrypt.kem import MLKEM_512, PQAVariant
from hashlib import pbkdf2_hmac
from pathlib import Path
import os

kem = MLKEM_512(PQAVariant.REF)

# file locations
publicKeyFile="keys/kPk.key"
secretKeyFile="keys/kSk.key"

# Generate sudo files
# https://docs.python.org/3/library/os.html
def genSudoFile(filePath):
    try:
        path = Path(filePath)
        dir = path.parent
        # Set up directory
        dir.mkdir(exist_ok=True)
        dir.chmod(0o700)
        print(bcolors.OKGREEN + "Generated: " + str(dir) + " & " + str(path) + bcolors.ENDC)
    except Exception as e:
        print(f"Process Error {e}")
        return None

# Get pubkey
def readFromFile(file):
    with open(file,"rb") as f:
        return f.read()

# Writing data to a file
def writeToFile(file, data):
    with open(file,"wb") as f:
        f.write(data)

# Generate and save private/public keys ~ TODO make files private
# writeToFileEnc(path, password, data):
def kyberGenKeys(password):
    # Generate kyber keys
    pk,sk = kem.keygen()
    # Write keys to file
    writeToFile(publicKeyFile, pk)
    # Encrypt private key
    writeToFileEnc(secretKeyFile, password,sk)
    print(bcolors.OKGREEN + "Wrote keys to files: " + publicKeyFile + secretKeyFile + bcolors.ENDC)

# Encrypt data
def kyberEncapsulate(publicKey):
    cipherText, sharedSecret = kem.encaps(publicKey)
    return cipherText, sharedSecret

kyberSecret = None
# Decrypt data
def kyberDecapsulate(cipherText, password=b"password"):
    global kyberSecret
    if kyberSecret is None:
        kyberSecret = readFromFileEnc(secretKeyFile,password)
    sharedSecret = kem.decaps(kyberSecret, cipherText)
    return sharedSecret

# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
def encAes(data, aesKey):
        # aes key generated from Kyber shared secret
        cipher = AES.new(aesKey, AES.MODE_EAX)
        # Generate nonce
        nonce = cipher.nonce
        # Encrypt the data
        ciphertext,tag = cipher.encrypt_and_digest(data)
        # Return nonce and ciphertext ~ to be posted to data stream
        return(nonce,ciphertext,tag)

# Decrypting AES using KyberCipherText, shared nonce, and ciphertext
def decAes(kCipherText, nonce, cipherText, tag, password=b"password"):
        # Convert to bytes
        kCipherText = bytes.fromhex(kCipherText)
        nonce = bytes.fromhex(nonce)
        cipherText = bytes.fromhex(cipherText)
        tag = bytes.fromhex(tag)
        # Get the shared secret from the kyber ciphertext
        aesKey = kyberDecapsulate(kCipherText,password)
        # Decrypt AES
        cipher = AES.new(aesKey, AES.MODE_EAX, nonce=nonce)
        decrypted = cipher.decrypt(cipherText)
        try:
                # Verify tag for authenticity
                cipher.verify(tag)
                # Convert to json
                return decrypted.decode("utf-8")
        except:
                print(bcolors.FAIL + "Invalid Tag" + bcolors.ENDC)

# Convert log to binary, encrypt with AES, return JSON data for upload
def logEncryptor(log):
    # Convert log to binary
    binaryLog = log.encode('utf-8')
    publicKey = readFromFile(publicKeyFile)
    # Get kyber shared secret and ciphertext
    kCipherText, ksharedsecret = kyberEncapsulate(publicKey)
    # AES encrypt the log using hashed kyber generated shared secret
    nonce,cipherText,tag = encAes(binaryLog, ksharedsecret)
    # Data for posting to data stream
    data = {
        "kyberct":kCipherText.hex(),
        "nonce":nonce.hex(),
        "log":cipherText.hex(),
        "tag":tag.hex()}
    return data

# https://docs.python.org/3/library/hashlib.html
def writeToFileEnc(path, password, data):
    # Get AES key
    # Generate hash of password for bcrypt
    salt = os.urandom(16)
    # Number of iteration
    iterations = 500_000
    # String to bytes
    # Using password generate new AES key
    key = pbkdf2_hmac("sha256",password,salt,iterations,dklen=32)
    # Encrypt the data
    nonce,ciphertext,tag = encAes(data, key)
    
    encData = salt + nonce + tag + ciphertext
    writeToFile(path,encData)

def readFromFileEnc(path, password):
    try:
        # slice up encrypted file
        enc = readFromFile(path)
        salt = enc[:16]
        nonce = enc[16:32]
        tag = enc[32:48]
        cipherText = enc[48:]

        iterations = 500_000
        # regen the AES key from supplied password
        aesKey = pbkdf2_hmac("sha256",password,salt,iterations,dklen=32)
        # Decrypt AES
        cipher = AES.new(aesKey, AES.MODE_EAX, nonce=nonce)
        decrypted = cipher.decrypt(cipherText)
        try:
            # Verify tag for authenticity
            cipher.verify(tag)
            # Convert to json
            return decrypted
        except:
            print(bcolors.FAIL + f"Invalid Tag {e}" + bcolors.ENDC)
    except Exception as e:
        print(bcolors.FAIL + f"FAIL: {e}" + bcolors.ENDC)