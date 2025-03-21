import json
from collections import Counter

# Filter the logs
def filterLog(jsonOut, dataName):
    return [jData for jData in jsonOut if jData["data"]["Type"]==dataName]

# Get log id's
def addId(log, dataName):
    # id = []
    # for jLine in log:
    #         if dataName == "LogId":
    #             if jLine["data"][dataName] not in id:
    #                 return(jLine["data"][dataName])
    #         elif dataName == "LineId":
    #             if jLine["data"][dataName] not in id:
    #                 return(jLine["data"][dataName])
    ids = [jLine["data"][dataName] for jLine in log]
    print(ids)
    return Counter(id["data"][dataName] for id in ids)

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
        # Gather Id's
        winLogIds = addId(winLogs, "LogId")
        linLogIds = addId(linLogs, "LineId")
        print("Win Id's", winLogIds)
        #Id count
        # winIdCount = Counter(jline["data"]["LogId"] for jline in winLogs)
        # Declare list of id's ~ This can be used to check for what should be there
        
        # print(winIdCount)