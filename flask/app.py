from flask import Flask, jsonify, request, render_template
from flask_paginate import Pagination, get_page_args
# To use methods Sam wrote : from [name.py] import [method_name] e.g. look below this line
from logReader import readDecryptSave
import json
from cryptoUtils import readFromFileEnc
from userInterface import getPassword, selectionValidator
from colours import bcolors
# https://flask.palletsprojects.com/en/stable/quickstart/

# Where stream data decrypted is located
path = "/logChain/app/streamDataDec.json"
copyPath = "/logChain/app/streamDataEnc.json"

app = Flask(__name__)

# Get data
keyPass = getPassword(bcolors.WARNING + "Enter Password for File Encryption: " + bcolors.ENDC, True)
logPass = getPassword(bcolors.WARNING + "Enter Password for Log Encryption: " + bcolors.ENDC, False)

webSelection = input(bcolors.WARNING + f"Start Web Page: y/n\n" + bcolors.ENDC)
webSelection = selectionValidator(webSelection)

readDecryptSave(path,copyPath,"data", keyPass, logPass, webSelection)

# Pagintation
# https://www.reddit.com/r/flask/comments/xy4t9o/pagination_with_json/
@app.route("/")
def displayLog():
    global keyPass, logPass
    # Run readDecryptSave to get the current status of the file
    readDecryptSave(path,copyPath,"data", keyPass, logPass, True)

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

    # Pagination
    page = int(request.args.get('page', 1))
    per_page = 20 
    offset = (page - 1) * per_page 
    items_pagination = logs[offset:offset+per_page] 
    total = len(logs) 
    pagination = Pagination(page=page, per_page=per_page, offset=offset, total=total, css_framework='bootstrap3') 
    return render_template('index.html', logs=items_pagination, keys=logKeys, pagination=pagination)

# https://stackoverflow.com/questions/29882642/how-to-run-a-flask-application
if __name__ == "__main__" and webSelection:
    app.run(host="0.0.0.0", port="8000")


# def login():
#     # user logs in and check for psswd
#     username = ""
#     loginData = {
#         "username":username,
#         "time":getTime()
#     }
    
#     addToStream("login","genesis",loginData)