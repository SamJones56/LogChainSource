import json
from collections import Counter

# Filter the logs
def filterLog(jsonOut, dataName):
    return [jData for jData in jsonOut if jData["data"]["Type"]==dataName]

# Get count of log id's
def addId(log, dataName):
    ids = [jLine["data"][dataName] for jLine in log]
    counter =  Counter(ids)
    return counter.items()

# Compare log files that are present
def compEntry(log, count):
    # Split count
    for logIds, freqs in count:
        # Loop through each log id and validate
        for freq in freqs:
            for logId in logIds:
                # Compare instances of log files at ids if they match
                temp = []
                
        # entries = [jLine["data"] for jLine in log]
    # print(entries)
    


# https://likegeeks.com/count-json-array-elements-python/#:~:text=7%20Benchmark%20Test-,Using%20len()%20Function,arrays%20>
# https://www.w3schools.com/python/python_lists_comprehension.asp
# https://flexiple.com/python/calculate-number-occurrences-list

# Split logs
# Get count of what id's are present
# Compare present id's
# Look for missing id's?


def logCompare(fileName):
    # Valid for Windows
    with open(fileName,"r") as f:
        # Read from json
        jsonOut = json.load(f)

        # Filter & split logs
        winLogs = filterLog(jsonOut,"Windows")
        linLogs = filterLog(jsonOut,"Linux")

        # Gather count of Id's
        winLogCount = addId(winLogs, "LogId")
        linLogCount = addId(linLogs, "LineId")
        print("Win Id's", winLogCount)
        print("Linux Id's", linLogCount)  

        # Compare log files that are present
        test = compEntry(winLogs, winLogCount)
        test = compEntry(linLogs, winLogCount)
