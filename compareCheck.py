import json


def filterLog(jsonOut, name):
    return [jData for jData in jsonOut if jData["data"]["Type"]==name]

def addId(log, dataName, id):
    for jLine in log:
            if jLine["data"][dataName] not in id:
                return jLine["data"]["LogId"]

# https://likegeeks.com/count-json-array-elements-python/#:~:text=7%20Benchmark%20Test-,Using%20len()%20Function,arrays%20>
# https://www.w3schools.com/python/python_lists_comprehension.asp
def logCompare(fileName):
    # Valid for Windows
    with open(fileName,"r") as f:
        # Read from json
        jsonOut = json.load(f)

        # Filter logs
        winLogs = filterLog("Windows")
        linLogs = filterLog("Linux")

        # Declare list of id's ~ This can be used to check for deletion of data
        wId = []
        lId = []
        # Add unique id's to the lists
        wId.append(addId(winLogs, "LogId", wId))
        wId.append(addId(linLogs, "LogId", lId))


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