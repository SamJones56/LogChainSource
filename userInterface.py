from colours import bcolors
from pathlib import Path





# Get user input
# https://www.w3schools.com/python/ref_string_format.asp
# https://docs.python.org/3/library/pathlib.html
def dataSelector():
    # declare supported filetypes
    supportedFileTypes = [".log",".csv"]
    # Get the FilePath and fileName
    filePath =  input(bcolors.WARNING + f"Enter Path to Log File:\n")
    path = Path(filePath)
    fileName = path.name
    # Check for validity
    if path.exists() and path.is_file():
        if path.suffix not in supportedFileTypes:
            print(bcolors.FAIL + f"Unsupported file type: {path.suffix}" + bcolors.ENDC)
            exit()
    else:
        print(bcolors.FAIL + f"Invalid file path: {path}" + bcolors.ENDC)
        exit()


    # # Get fileType
    # fileType = input(bcolors.WARNING + f"Log Types: {fileTypes} \n Selection:" + bcolors.ENDC)
    # # Check if valid
    # if fileType not in fileTypes:
    #     print(bcolors.FAIL + f"Invalid file type: {fileType}" + bcolors.ENDC)
    #     exit()
    # print(bcolors.OKGREEN, fileType, bcolors.ENDC)
    # # Defaults
    # streamName = "data"

    # if fileType == 1:
    #     filePath = "winTest.csv"
    #     key = "Node1"
    # elif fileType == 2:
    #     filePath = "linTest.csv"
    #     key = "Node2"
    # else:
    #     print(bcolors.FAIL + "Invalid file type: ", fileType, bcolors.ENDC)
    #     exit()
    # print(bcolors.OKGREEN, filePath, fileType, streamName, key, bcolors.ENDC)
    # return filePath, fileType, streamName,key