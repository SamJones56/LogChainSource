# https://flask.palletsprojects.com/en/stable/quickstart/
from flask import Flask, jsonify, request, render_template
from logReader import readDecryptSave
import json

# USAGE
# python3 ../flask/app.py


decryptedFilepath = "/logChain/app/streamDataDec.json"

app = Flask(__name__)

@app.route("/")
def hello_world():
    # Run readDecryptSave to get the current status of the file
    readDecryptSave("/logChain/app/streamDataDec.json", "data")

    # https://medium.com/@junpyoo50/transforming-json-input-into-html-table-view-with-flask-and-jinja-a-step-by-step-guide-1d62e2fa49ed
    # init logs and listkeys
    logs = []
    listKeys = []
    # Open decrypted file from blockchain
    with open(decryptedFilepath,"r") as logFile:
        # read through the open file
        for logLine in logFile:
            try:
                # save each of the lines as a json log entry
                logEntry = json.loads(logLine)
                # add logs to the logs variable
                logs.append(logEntry)
                # Set the list keys - used in table header
                listKeys = list(logEntry.keys())
            
            # throw error
            except Exception as e:
                print(f"e")
    # Render index.html with the data
    return render_template('index.html', logs=logs, keys=listKeys)

# https://stackoverflow.com/questions/29882642/how-to-run-a-flask-application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")