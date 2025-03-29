# https://pypi.org/project/watchdog/
import time
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from sh import tail
from pathlib import Path
import os.path
from mcController import addToStreamOptions#
import json

# from logPoster import postToChain, getFileHash
# data -> JSON for blockchain
def blockConverter(fileType,hashDigest,log):
    # Data for identification
    entry = {
        "Type":fileType,
        "FileHash":hashDigest,
    }
    entry.update(log)
    return entry

def postToChain(key, fileType, hashDigest, log, streamName):
    data = blockConverter(fileType,hashDigest,log)
    # Add to the data stream
    data = {"json":data}
    print("added")
    addToStreamOptions(streamName, key, data, "offchain")
# postToChain(key, fileType, hashDigest, log, streamName)

def doggy(filePath, hashDigest, key, fileType, streamName):
    filePath=[f"{filePath}"]

    #converts paths from list to string and then converts to special path for file check
    pathString=''.join(map(str, filePath))
    checkPath= Path(pathString)
    # fileList = [filePath]
    ##Class for monitor rules, defines what happens when a file is modified or deleted using a pattern
    class Monitorclass(PatternMatchingEventHandler):
        
        #pattern for monitoring pulled from filepath defined
        patterns=filePath
        #rules for printing that the file has been modified, to be replaced with reading the last line of the file
        #and uploading it, with an exception for if there is no file anymore
        def on_modified(self, event):
                #check for if the file exists, else outputs an error
                if checkPath.is_file():
                    #prints last line on unix system
                    for line in tail("-n 1",filePath, _iter=True):
                        line = line.strip()
                        if not line:
                            continue
                        log = {line}
                        # update
                        print(log)
                        postToChain(key, fileType, hashDigest, log, streamName)


                else:
                    print("oopsie, ya file got gone")

    event_handler = Monitorclass()
    observer= Observer()
    #code for the observer to only look in the path given, as well as recursive loop that keeps it going and allows keyboard interrupt.
    for path in filePath:
        observer.schedule(event_handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join
