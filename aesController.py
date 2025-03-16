from Crypto.Cipher import AES

def encAes(data, aesKey):
        # encKey = os.urandom(32)
        cipher = AES.new(aesKey, AES.MODE_EAX)

        nonce = cipher.nonce
        ciphertext, tag = cipher.encrypt_and_digest(data)

        return(nonce,ciphertext)

# def decAes(kCipherText, nonce, cipherText):
