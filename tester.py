from mcController import getStreamData
from aesController import decAes
from colours import bcolors
from compareCheck import logCompare
import json
import time
# https://www.geeksforgeeks.org/reading-and-writing-json-to-a-file-in-python/
# Writing data to a file
def writeToFile(file, data):
    with open(file,"w") as f:
        json.dump(data, f)

# Read and decrypt
def readDecryptSave(jsonOut):
    # Store output
    jDecrypted = []
    # Loop through the json output
    for jLine in jsonOut:
        # Get the publishers and keys
        publishers = jLine['publishers']
        key = jLine["keys"]
        # Gather info from json
        jData = jLine["data"]["json"]
        kyberct = jData["kyberct"]
        nonce = jData["nonce"]
        cipherText = jData["data"]
        tag = jData["tag"]

        # Decrypt the json
        jDecrypt = decAes(kyberct,nonce,cipherText,tag)
        # Remove nested
        if "json" in jDecrypt:
            jDecrypt=jDecrypt["json"]
        
        data = {
            "walletAddress":publishers,
            "nodeKey":key,
            "data":jDecrypt
        }
        
        # Append to jDecrypted
        jDecrypted.append(data)
    # Save the final list    
    writeToFile("streamDataDec.json", jDecrypted)

# Get the data from sthe stream
streamData = getStreamData("data", False)
readDecryptSave(streamData)
# logCompare("streamDataDec.json")

# "reload button" clicked -> 
# 1. Call -> streamData = getStreamData("data", False)  :: Gets current data stream data 
# 2. readDecryptSave(streamData)                        :: Decryptes the data stream and saves it to "streamDataDec.json"
# Extra. logCompare("streamDataDec.json")               :: Is how we compare the decoded json file


OrderedDict({
    'publishers': ['18JVKSZMAk3LUNAJzkTVBbYgyBqhBDkMnSm8BG'], 
    'keys': ['node1'], 
    'offchain': False, 
    'available': True, 
    'data': 
        OrderedDict({
            'json': 
                OrderedDict({
                    'Type': 'winTest.csv', 
                    'FileHash': '903256c7c86d9ef4a6d218229d0a75ed7bffe6de46727b9fdb9f9581ef270d1b', 
                    'kyberct': 'f27e046b2ddb16d9dde208e2608e9ce9517b92a5fff5ea3f698c5f03db982209020d26538b0ba223889c0a23d23a31622e5931f8e07ae4cf4780fdb4be8a4dfad757934c06c8ce3ca61b7bff3494ccfb94bede14a55d83a8569517478da9a8c99e733187b128f342cea5f51f70fb5cd6acf15ff0ad91eecaaa7bf56b1cc3a13726bc809a42b6e7542a98975a6cde6b0111565b6f5f4fc18c78599a72125da600556c5f263a2b3119ed9baf0952f786f85fc1304ea1862b38a3aa4900f2e6e97f8476fd4a9e9acb497ed0c86b2421a073da004096f893db0db98200d52c1c9bf0d075ff05eda7adb1a75e42f21d44052232918d5a3ea866dca8c159bf5a5b23faecfcb6a85c0c83765b3d5ca24abe0fc25004995cb71c8a7c3371cfad5c99bb56f2bad5f45db8c913d28921be343e3feb88013b44126583d89a1703ff1d93eb3de86c28ae1ac633ce2acb127dc10860a83fc966454867093bb3d7166afe098319561eb323692e444ebc633918485430c9bbe87e2bded2a573ddeed2d829c33f85342fbeb0913bd1fe33599d62204493dbe7e0ea52e1612269251d7cb0714f80c997cbb1cebd84897ba0dae7cb80b90b93bfc699863bf5c4fbdacd210c1a3e6fe65442ccefaadf15ab2fa348072f3ce0c841713c309f1373c3c2e82b0d28122a0bc96d6c8617cfdc4712a45819db2bb750b49d155a2bc4291f205692a5215f8c52e62508b7f83b78f506eb1ee99bffb49dfddcce563afcf1a0f10366dd54e11f0d64db36baa025b70965978d5f6b328fa22f7256030e57a251be9eccc30453f1647f610970b7d2da83921184d8db2017909bafc5445009f48c0393471d64d42bbe067534902f8698f0a27eaedd33bc3dbfefb415e693830cb82368b74121b3ff458e2a406f0ad484ec0b562a8edb06564cd424d24b34e90df48ca0a3f7f74fe608a8d2d685d1a62a0f610ee65351bdaec85000cd1276b54f4fd14a75bcdc33385f6f69086df60cf252e07bc12a366754188c7ff7b3c3069edb39689755c25b554f312b980a17681c4195c813d8e8c8d49fe8f29e15cb41474a953e24fefe552ea1',
                    'nonce': '7380101b04f2fc654773c8e50567179e', 
                    'log': 'f67eb7cc62ce1b4b852a9bff978f57a1a96e8aef6617c46cb5d12272fc1d57a554c3aa9641c953938baa1e18a6aac6fc27bce634c3d8a489b49d67f07f4282bbda7800adf07e721a39ecbe253b3522478194f5ca144e4188c25dc6f436a4a08ba9e4d45cc5cfb9ad3d8435012cdaf778e05e29339fbbebd1ff527f5f584dcf461a1707121f55840cb141e7b1860b001f86e0f47e54e63646603207577f2633739b06205433a8f8d04cea679858', 
                    'tag': '7a67ea1b2202a04c25148a441ad3bf7f'
                })
        }), 
    'confirmations': 11, 
    'blocktime': 1742838404, 
    'txid': 'ea22d8bf8113d8c5118cfe1e9aa1c84b412b89efc812458919c0c2fdff5c0ec3'})