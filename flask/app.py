# https://flask.palletsprojects.com/en/stable/quickstart/
from flask import Flask, jsonify, request, render_template
# To use methods Sam wrote : from [name.py] import [method_name] e.g. look below this line
from logReader import readDecryptSave
from mcController import addToStream
import json
from cryptoUtils import readFromFileEnc

# USAGE
# ./web.sh

# Where stream data decrypted is located
path = "/logChain/app/streamData.json"

app = Flask(__name__)

@app.route("/")
def displayLog():
    # Run readDecryptSave to get the current status of the file
    readDecryptSave(path, "data")

    # https://medium.com/@junpyoo50/transforming-json-input-into-html-table-view-with-flask-and-jinja-a-step-by-step-guide-1d62e2fa49ed
    # init logs and listkeys
    logs = []
    logKeys = []
    # Open decrypted file from blockchain
    # with open(decryptedFilepath,"r") as logFile:
    password = b"password"
    logFile = readFromFileEnc(path, password)
    # read through the open file
    # log file = data of the entire file
    # log line = each line in the logFile ~ for loop
    for logLine in logFile:
        try:
            # save each of the lines as a json log entry
            logEntry = json.loads(logLine)
            # add logs to the logs variable
            logs.append(logEntry)
            # Set the list keys - used in table header
            logKeys = list(logEntry.keys())
        
        # throw error
        except Exception as e:
            print(f"e")
    # Render index.html with the data
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