# https://pypi.org/project/watchdog/
import time
from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer
from sh import tail
from pathlib import Path
import os.path
from colours import bcolors
# from mcController import addToStreamOptions
import json
from utils import logEncryptor, getFileHash, postToChain

# https://www.askpython.com/python/built-in-methods/callback-functions-in-python
def doggy(filePath, fileType, key, streamName):
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
                        hashDigest = getFileHash(pathString)
                        log = logEncryptor(line)
                        print(bcolors.WARNING + f"Ammending to {streamName} Stream\n" + bcolors.OKBLUE + f"{line}" + bcolors.ENDC)
                        postToChain(key, fileType, hashDigest, log, streamName)
                        # update
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
