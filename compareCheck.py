import json
from collections import Counter
import hashlib
from colours import bcolors
# https://stackoverflow.com/questions/65561243/print-a-horizontal-line-in-python
import os

# Get terminal size for hr
term_size = os.get_terminal_size()

# https://likegeeks.com/count-json-array-elements-python/#:~:text=7%20Benchmark%20Test-,Using%20len()%20Function,arrays%20>
# https://www.w3schools.com/python/python_lists_comprehension.asp
# https://flexiple.com/python/calculate-number-occurrences-list

# Filter the logs
def filterLog(jsonOut, key, value):
    return [jData for jData in jsonOut if jData["data"][key]==value]

# Get count of log id's
def addId(log, dataName):
    ids = [jLine["data"][dataName] for jLine in log]
    counter = Counter(ids)
    return counter.items()

# CANT HAVE MORE 6'S THAN FIVES - CHECK HERE FOR THAT BUT US X'S AND Y'S

# Find errors https://stackoverflow.com/questions/1388818/how-can-i-compare-two-lists-in-python-and-return-matches
def errorLocator(currentEntry, prevEntry):
    return set(currentEntry.items()) ^ set(prevEntry.items())
        

# Check data against previous entry
def recursiveCheck(entries):
    # Check for 0 length
    if len(entries) < 2:
        return
    # Previous entry
    prevEntry = None
    # Loop through entries
    errorIndex = 0
    # Loop through entries
    
    for index, entry in enumerate(entries):
        if prevEntry != None:
            # Compare entries
            if entry == prevEntry:
                #print(bcolors.OKGREEN + f"Entries Match \n" + 
                print(bcolors.OKGREEN + f"Entry: {index-1}\n" +
                bcolors.OKCYAN + f"{prevEntry}\n" +
                bcolors.OKGREEN + f"Matches Entry: {index}\n" +
                bcolors.OKCYAN + f"{entry}" + bcolors.ENDC)
            else:
                errorIndex = index
                error = errorLocator(entry["data"], prevEntry["data"])
                
                print(bcolors.FAIL + f"MISSMATCH DETECTED \n" + 
                bcolors.FAIL + f"Entry: {index-1}\n" +
                bcolors.WARNING + f"{prevEntry}\n" +
                bcolors.FAIL + f"Does Not Match Entry: {index}\n" +
                bcolors.WARNING + f"{entry}" + bcolors.ENDC)
                print(error)
            if errorIndex > 0:
                print(bcolors.FAIL + f"PREVIOUS MISSMATCH DETECTED AT LOG ENTRY {errorIndex}." + bcolors.ENDC)
                print(bcolors.FAIL + '^' * term_size.columns + bcolors.ENDC)
        prevEntry = entry


# Compare log files that are present
def compEntry(log, count, idType):
    # Split count
    for logId, freq in count:
        # Loop through entries in log and check if they have correct data type
        entries = [jLine for jLine in log if jLine["data"][idType] == logId]
        # Printing for entries
        # print(bcolors.OKGREEN + '=' * term_size.columns, bcolors.ENDC) 
        # Check entries
        recursiveCheck(entries)
        print(bcolors.OKGREEN + '=' * term_size.columns, bcolors.ENDC)


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
