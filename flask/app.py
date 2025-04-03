# https://flask.palletsprojects.com/en/stable/quickstart/
from flask import Flask, jsonify, request, render_template
# To use methods Sam wrote : from [name.py] import [method_name] e.g. look below this line
from logReader import readDecryptSave
import json
from cryptoUtils import readFromFileEnc
from userInterface import getPassword
from colours import bcolors

# USAGE
# ./web.sh

# Where stream data decrypted is located
path = "/logChain/app/streamDataDec.json"
copyPath = "/logChain/app/streamDataEnc.json"

app = Flask(__name__)

keyPass = getPassword(bcolors.WARNING + "Enter Password for File Encryption: " + bcolors.ENDC)
logPass = getPassword(bcolors.WARNING + "Enter Password for Log Encryption: " + bcolors.ENDC)

readDecryptSave(path,copyPath,"data",keyPass,logPass)

@app.route("/")
def displayLog():
    global keyPass, logPass
    # Run readDecryptSave to get the current status of the file
    # readDecryptSave(path,copyPath,"data", keyPass, logPass)

    # https://medium.com/@junpyoo50/transforming-json-input-into-html-table-view-with-flask-and-jinja-a-step-by-step-guide-1d62e2fa49ed
    # init logs and listkeys
    logs = []
    logKeys = []
    # password = b"password"
    # logFile = readFromFileEnc(copyPath, logPass)
    logFile = readFromFileEnc(path, logPass)

    logLines = logFile.splitlines()
    for line in logLines:
        logs.append(json.loads(line))
    logKeys = list(logs[0].keys())

    return render_template('index.html', logs=logs, keys=logKeys)

# https://stackoverflow.com/questions/29882642/how-to-run-a-flask-application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")


# def login():
#     # user logs in and check for psswd
#     username = ""
#     loginData = {
#         "username":username,
#         "time":getTime()
#     }
    
#     addToStream("login","genesis",loginData)