import json
from collections import Counter

# Filter the logs
def filterLog(jsonOut, dataName):
    return [jData for jData in jsonOut if jData["data"]["Type"]==dataName]

# Get count of log id's
def addId(log, dataName):
    ids = [jLine["data"][dataName] for jLine in log]
    return Counter(ids)

#def contOccurance

# https://likegeeks.com/count-json-array-elements-python/#:~:text=7%20Benchmark%20Test-,Using%20len()%20Function,arrays%20>
# https://www.w3schools.com/python/python_lists_comprehension.asp
# https://flexiple.com/python/calculate-number-occurrences-list
def logCompare(fileName):
    # Valid for Windows
    with open(fileName,"r") as f:
        # Read from json
        jsonOut = json.load(f)

        # Filter logs
        winLogs = filterLog(jsonOut,"Windows")
        linLogs = filterLog(jsonOut,"Linux")
        # Gather count of Id's
        winLogIds = addId(winLogs, "LogId")
        linLogIds = addId(linLogs, "LineId")
        print("Win Id's", winLogIds)
        print("Linux Id's", linLogIds)