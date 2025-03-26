# https://flask.palletsprojects.com/en/stable/quickstart/
from flask import Flask
from app.logReader import readDecryptSave


decryptedFilepath = "streamDataDec.txt"
# Start webpage
# flask --app ../flask/app.py run --host=0.0.0.0 --port=8000

app = Flask(__name__)

@app.route("/")
def hello_world():
    # Run readDecryptSave to get the current status of the file
    readDecryptSave("streamDataDec.txt", "data")

    with decryptedFilepath.open("r") as logFile:
        for logLine in logFile:
            return f"{logLine}"

    # return "<p>Hello, World!</p>"