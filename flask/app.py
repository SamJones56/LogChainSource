# https://flask.palletsprojects.com/en/stable/quickstart/
from flask import Flask
from logReader import readDecryptSave


# flask --app ../flask/app.py run --host=0.0.0.0 --port=8000

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"