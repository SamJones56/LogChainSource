# https://pypi.org/project/watchdog/
import time
from watchdog.events import PatternMatchingEventHandler
from watchdog.events import FileModifiedEvent
from watchdog.observers import Observer

filePath=["/home/lilith/src/paper"]

##Class for monitor rules, defines what happens when a file is modified or deleted using a pattern
class Monitorclass(PatternMatchingEventHandler):
    #pattern for monitoring pulled from filepath defined
    patterns=filePath
    #rules for printing that the file has been modified, to be replaced with reading the last line of the file
    #and uploading it, with an exception for if there is no file anymore
    def on_modified(self, event):
            print(f"file modified: {event.src_path}")
    
    def on_deleted(self, event):
            print(f"file deleted: {event.src_path}")

event_handler = Monitorclass()
observer= Observer()
#code for the observer to only look in the path given, as well as recursive loop that keeps it going and allows keyboard interrupt.
for path in filePath:
    observer.schedule(event_handler, path, recursive=True)
observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
     observer.stop()
observer.join
