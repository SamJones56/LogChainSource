from flask import Flask, jsonify, request, render_template
from flask_paginate import Pagination, get_page_args
# To use methods Sam wrote : from [name.py] import [method_name] e.g. look below this line
from logReader import readDecryptSave
import json
import threading
import time
from cryptoUtils import readFromFileEnc
from userInterface import getPassword, selectionValidator
from colours import bcolors
# https://flask.palletsprojects.com/en/stable/quickstart/

# Where stream data decrypted is located
path = "/logChain/app/streamDataDec.json"
copyPath = "/logChain/app/streamDataEnc.json"

app = Flask(__name__)

# Get data
keyPass = getPassword(bcolors.WARNING + "Enter Password for Decryption: " + bcolors.ENDC, True)
logPass = getPassword(bcolors.WARNING + "Enter Password for Log Encryption: " + bcolors.ENDC, False)

webSelection = input(bcolors.WARNING + f"Start Web Page: y/n\n" + bcolors.ENDC)
webSelection = selectionValidator(webSelection)

if webSelection == False:
    readDecryptSave(path,copyPath,"data", keyPass, logPass, webSelection)

# https://stackoverflow.com/questions/34749331/running-a-background-thread-in-python
def logThread():
    while True:
        readDecryptSave(path,copyPath,"data", keyPass, logPass, True)
        time.sleep(5)


def oldNew(new, logLines):
    logs = []
    if(new):
        for line in logLines:
            logs.append(json.loads(line))
    else:
        for line in reversed(logLines):
            logs.append(json.loads(line))
    return logs


# Pagintation
# https://www.reddit.com/r/flask/comments/xy4t9o/pagination_with_json/
@app.route("/")
def displayLog():
    global keyPass, logPass
    # https://medium.com/@junpyoo50/transforming-json-input-into-html-table-view-with-flask-and-jinja-a-step-by-step-guide-1d62e2fa49ed
    # init logs and listkeys
    logs = []
    logKeys = []
    logFile = readFromFileEnc(path, logPass)
    

    # https://www.geeksforgeeks.org/backward-iteration-in-python/
    logLines = logFile.splitlines()
    # for line in reversed(logLines):
    #     logs.append(json.loads(line))
    # Old or new selector
    sortOrder = request.args.get('sortOrder','')
    if sortOrder == 'newest':
        new = True
    else:
        new = False

    logs = oldNew(new, logLines)
    logKeys = list(logs[0].keys())

    # Pagination
    page = int(request.args.get('page', 1))
    # Get the value from the webpage
    per_page = int(request.args.get('per_page', 50)) 
    searchBar = request.args.get('searchBar','')
    dateFrom = request.args.get('dateFrom','')
    dateTo = request.args.get('dateTo','')
    offset = (page - 1) * per_page 
    items_pagination = logs[offset:offset+per_page] 
    total = len(logs) 
    pagination = Pagination(page=page, 
                            per_page=per_page, 
                            offset=offset, 
                            total=total, 
                            href='?page={0}'+
                            '&per_page=' + str(per_page)+ 
                            '&searchBar='+searchBar+
                            '&dateFrom='+dateFrom+
                            '&dateTo='+dateTo) 
    return render_template('index.html', 
                           logs=items_pagination, 
                           keys=logKeys, 
                           pagination=pagination, 
                           per_page = per_page, 
                           searchBar=searchBar,
                           dateTo=dateTo,
                           dateFrom=dateFrom,
                           new=new)

# https://stackoverflow.com/questions/29882642/how-to-run-a-flask-application
if __name__ == "__main__" and webSelection:
    # Start thread
    updateThread = threading.Thread(target=logThread, daemon=True)
    updateThread.start()
    app.run(host="0.0.0.0", port="8000")


# def login():
#     # user logs in and check for psswd
#     username = ""
#     loginData = {
#         "username":username,
#         "time":getTime()
#     }
    
#     addToStream("login","genesis",loginData)