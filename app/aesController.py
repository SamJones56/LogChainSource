from Crypto.Cipher import AES
from colours import bcolors

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
def decAes(kCipherText, nonce, cipherText, tag):
        from kyberController import decapsulate
        # Convert to bytes
        kCipherText = bytes.fromhex(kCipherText)
        nonce = bytes.fromhex(nonce)
        cipherText = bytes.fromhex(cipherText)
        tag = bytes.fromhex(tag)
        # Get the shared secret from the kyber ciphertext
        aesKey = decapsulate(kCipherText)
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