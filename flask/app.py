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

    logs = []
    listKeys = []

    with open(decryptedFilepath,"r") as logFile:
        # Save the log entry
        for logLine in logFile:
            try:
                logEntry = json.loads(logLine)
                logs.append(logEntry)
                if not listKeys:
                    listKeys = list(logEntry.keys())
                # logs.append(data)
                
            except Exception as e:
                print(f"e")
    return render_template('index.html', logs=logs, keys=listKeys)


        # return jsonify(logs)

    # return "<p>Hello, World!</p>"
# https://stackoverflow.com/questions/29882642/how-to-run-a-flask-application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")