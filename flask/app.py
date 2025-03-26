# https://flask.palletsprojects.com/en/stable/quickstart/
# https://www.geeksforgeeks.org/use-jsonify-instead-of-json-dumps-in-flask/
from flask import Flask, jsonify
import json
from logReader import readDecryptSave

# USAGE
# python3 ../flask/app.py


decryptedFilepath = "streamDataDec.txt"

app = Flask(__name__)

@app.route("/")
def hello_world():
    # Run readDecryptSave to get the current status of the file
    readDecryptSave("../flask/streamDataDec.txt", "data")

    logs = []
    with open(decryptedFilepath,"r") as logFile:
        for logLine in logFile:
            # jsonData = json.dumps(logLine)
            jsonData = jsonify({logLine:"data"})
            return f"{jsonData}\n<hr>"



    # return "<p>Hello, World!</p>"
# https://stackoverflow.com/questions/29882642/how-to-run-a-flask-application
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8000")