from Crypto.Cipher import AES
from kyberController import decapsulate
# https://pycryptodome.readthedocs.io/en/latest/src/cipher/aes.html
def encAes(data, aesKey):
        # aes key generated from Kyber shared secret
        cipher = AES.new(aesKey, AES.MODE_EAX)
        # Generate nonce
        nonce = cipher.nonce
        # Encrypt the data
        ciphertext = cipher.encrypt_and_digest(data)
        # Return nonce and ciphertext ~ to be posted to data stream
        return(nonce,ciphertext)

# Decrypting AES using KyberCipherText, shared nonce, and ciphertext
def decAes(kCipherText, nonce, cipherText):
        # Convert to bytes
        kCipherText = bytes.fromhex(kCipherText)
        nonce = bytes.fromhex(nonce)
        cipherText = bytes.fromhex(cipherText)
        # Get the shared secret from the kyber ciphertext
        aesKey = decapsulate(kCipherText)
        # Decrypt AES
        cipher = AES.new(aesKey, AES.MODE_EAX, nonce=nonce)
        decrypted = cipher.decrypt(cipherText)
        return decrypted