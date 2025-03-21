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
def recursiveCheck(entries):
    # Check for 0 length
    if len(entries) < 2:
        return
    # Previous entry
    prevEntry = None
    # Loop through entries
    for index, entry in enumerate(entries):
        if prevEntry != None:
            # COmpare entries
            if entry == prevEntry:
                print(bcolors.OKGREEN + f"Entries Match \n" + 
                bcolors.OKBLUE + f"Checking entry: {index}\n" +
                bcolors.OKCYAN + f"{entry}\n" +
                bcolors.OKBLUE + f"Against entry: {index-1}\n" +
                bcolors.OKCYAN + f"{prevEntry}" + bcolors.ENDC)
            else:
                print(bcolors.FAIL + f"MISSMATCH DETECTED \n" + 
                bcolors.FAIL + f"Error Located: {index}\n" +
                bcolors.WARNING + f"{entry}\n" +
                bcolors.FAIL + f"Against entry: {index-1}\n" +
                bcolors.WARNING + f"{prevEntry}" + bcolors.ENDC)
        prevEntry = entry


# Compare log files that are present
def compEntry(log, count, idType, prevEntry=''):
    # Split count
    for logId, freq in count:
        # Loop through entries in log and check if they have correct data type
        entries = [jLine for jLine in log if jLine["data"][idType] == logId]
        # Check each entry against previous
        recursiveCheck(entries)


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
        test = compEntry(linLogs, linLogCount, "LineId")
