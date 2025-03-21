import json
from collections import Counter
import hashlib
from colours import bcolors

# https://likegeeks.com/count-json-array-elements-python/#:~:text=7%20Benchmark%20Test-,Using%20len()%20Function,arrays%20>
# https://www.w3schools.com/python/python_lists_comprehension.asp
# https://flexiple.com/python/calculate-number-occurrences-list

# Split logs
# Get count of what id's are present
# Compare present id's
# Look for missing id's?

# Filter the logs
def filterLog(jsonOut, dataName):
    return [jData for jData in jsonOut if jData["data"]["Type"]==dataName]

# Get count of log id's
def addId(log, dataName):
    ids = [jLine["data"][dataName] for jLine in log]
    counter =  Counter(ids)
    return counter.items()

# Sequencly check data against previous
def recursiveCheck(maxCount, entry,prevEntry=''):
    # Counter
    counter = 0
    # Break case
    if counter == maxCount:
        print(bcolors.OKCYAN + f"Check Completed" + bcolors.ENDC)
        return
    elif counter != 0:
        if entry == prevEntry:
            print(bcolors.OKGREEN + f"Entries Matched" + bcolors.ENDC)
            prevHash = entry
            entry = nextEntry
            counter 
            recursiveCheck(maxCount, entry, prevEntry)

# Compare log files that are present
def compEntry(log, count, idType, prevEntry=''):
    # Split count
    for logId, freq in count:
        # Loop through entries in log and check if they have correct data type
        entries = [jLine for jLine in log if jLine["data"][idType] == logId]
        print(f"Id {logId} occurs {freq} times: ")
        # Loop through entries ~ hash then comp
        for entry in entries:
            # Compare
            print(f"\n", json.dumps(entry))
            recursiveCheck(freq, entry)


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
        test = compEntry(winLogs, winLogCount, "LogId")
        test = compEntry(linLogs, winLogCount, "LineId")
