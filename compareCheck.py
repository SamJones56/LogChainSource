import json
from collections import Counter


def filterLog(jsonOut, dataName):
    return [jData for jData in jsonOut if jData["data"]["Type"]==dataName]

def addId(log, dataName):
    id = []
    for jLine in log:
            if jLine["data"][dataName] not in id:
                return id.append(jLine["data"]["LogId"])
            
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
        winLogs = filterLog("Windows")
        linLogs = filterLog("Linux")

        # Declare list of id's ~ This can be used to check for what should be there
        wId = addId(winLogs, "LogId")
        lId = addId(linLogs, "LineId")

        print(wId)
        print(lId)


        # # Loop through JSON lines in JSON output
        # for jLine in jsonOut:
        #     # Check if windows
        #     if jLine["data"]["Type"] == "Windows":
        #         if jLine["data"]["LogId"] not in ids:
        #             ids.append(jLine["data"]["LogId"])
        #             print(ids)
        #             test = "1"
        #             count = sum(1 for obj in jsonOut if obj["data"]["LogId"] == test)
        #             print(count)
        #     elif jLine["data"]["Type"] == "Linux":
        #         break