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

keyPass = getPassword(bcolors.WARNING + "Enter Password for File Encryption: " + bcolors.ENDC, True)
logPass = getPassword(bcolors.WARNING + "Enter Password for Log Encryption: " + bcolors.ENDC, False)

readDecryptSave(path,copyPath,"data",keyPass,logPass)

@app.route("/")
def displayLog():
    global keyPass, logPass

    # Get the filter string from the search box
    filter_query = request.args.get("filter", "").lower()

    logs = []
    logKeys = []

    # Decrypt log contents
    logFile = readFromFileEnc(path, logPass)
    logLines = logFile.splitlines()

    for line in logLines:
        try:
            logEntry = json.loads(line)
            # Only include logs that match the filter (if any)
            if not filter_query or any(filter_query in str(value).lower() for value in logEntry.values()):
                logs.append(logEntry)
                logKeys = list(logEntry.keys())
        except Exception as e:
            print(f"Error reading log line: {e}")

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