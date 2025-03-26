# https://flask.palletsprojects.com/en/stable/quickstart/
from flask import Flask, jsonify
from logReader import readDecryptSave

# USAGE
# python3 ../flask/app.py


decryptedFilepath = "/logChain/app/streamDataDec.json"

app = Flask(__name__)

@app.route("/")
def hello_world():
    # Run readDecryptSave to get the current status of the file
    readDecryptSave("/logChain/app/streamDataDec.json", "data")

    log = []

    with open(decryptedFilepath,"r") as logFile:
        # Save the log entry
        for logLine in logFile:
            log.append(logLine)

        entries = [jLine for jLine in log]
        # return f"{entries}\n<hr>"
        for index,entry in enumerate(entries):
            return f"{index} : {entry} \n"


    # return "<p>Hello, World!</p>"
# https://stackoverflow.com/questions/29882642/how-to-run-a-flask-application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")