import json
from collections import Counter
import hashlib
from colours import bcolors

# https://likegeeks.com/count-json-array-elements-python/#:~:text=7%20Benchmark%20Test-,Using%20len()%20Function,arrays%20>
# https://www.w3schools.com/python/python_lists_comprehension.asp
# https://flexiple.com/python/calculate-number-occurrences-list

# Filter the logs
def filterLog(jsonOut, key,value):
    #if ["data"] in jsonOut:
    return [jData for jData in jsonOut if jData["data"][key]==value]

# Get count of log id's
def addId(log, dataName):
    ids = [jLine["data"][dataName] for jLine in log]
    counter = Counter(ids)
    return counter.items()

# CANT HAVE MORE 6'S THAN FIVES - CHECK HERE FOR THAT BUT US X'S AND Y'S
# ADD FLAG FOR UNHAPPY IN RECURSION OR COLOUR CHANGE

# Check data against previous entry
def recursiveCheck(entries):
    # Check for 0 length
    if len(entries) < 2:
        return
    # Previous entry
    prevEntry = None
    # Loop through entries
    sadIndex = 0
    for index, entry in enumerate(entries):
        if prevEntry != None:
            # Compare entries
            if entry == prevEntry:
                print(bcolors.OKGREEN + f"Entries Match \n" + 
                bcolors.OKBLUE + f"Checking entry: {index}\n" +
                bcolors.OKCYAN + f"{entry}\n" +
                bcolors.OKBLUE + f"Against entry: {index-1}\n" +
                bcolors.OKCYAN + f"{prevEntry}" + bcolors.ENDC)
            else:
                sadIndex = index
                print(bcolors.FAIL + f"MISSMATCH DETECTED \n" + 
                bcolors.FAIL + f"Error located at entry: {index}\n" +
                bcolors.WARNING + f"{entry}\n" +
                bcolors.FAIL + f"Checked against entry: {index-1}\n" +
                bcolors.WARNING + f"{prevEntry}" + bcolors.ENDC)
            if sadIndex > 0:
                print(bcolors.FAIL + f"PREVIOUS MISSMATCH DETECTED IN LOG" + bcolors.ENDC)
        prevEntry = entry


# Compare log files that are present
def compEntry(log, count, idType):
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
        winLogs = filterLog(jsonOut,"Type","Windows")
        linLogs = filterLog(jsonOut,"Type","Linux")

        # Gather count of Id's
        winLogCount = addId(winLogs, "LogId")
        linLogCount = addId(linLogs, "LineId")

        # Compare log files that are present
        compEntry(winLogs, winLogCount, "LogId")
        compEntry(linLogs, linLogCount, "LineId")
