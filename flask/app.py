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
    list_key = []

    with open(decryptedFilepath,"r") as logFile:
        # Save the log entry
        for logLine in logFile:
            result = json.loads(logLine)
            list_key = list_key.append(list(result.keys()))
            # logs.append(data)
        return render_template('index.html', data = data_input, result = result, keys = list_key )

        # return jsonify(logs)

    # return "<p>Hello, World!</p>"
# https://stackoverflow.com/questions/29882642/how-to-run-a-flask-application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")