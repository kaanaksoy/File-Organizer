from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import json
import time
import re

from locations import folder_paths


folder_to_track = folder_paths['srcPath']
folder_destination = folder_paths['destRootPath']
finalDestination = ''

class MyHandler(FileSystemEventHandler):
    i = 1
    def on_modified(self, event):
        for filename in os.listdir(folder_to_track):
            fileClass = re.search("^\d\d[-]\d\d\d", filename)
            if (fileClass != None) and (fileClass.group() in folder_paths):
                finalDestination = folder_paths[fileClass.group()]
                src = folder_to_track + "/" + filename
                filename = filename[6:]
                new_destionation = folder_destination + finalDestination + "/" + filename
                os.rename(src, new_destionation)

event_handler = MyHandler()
observer = Observer()
observer.schedule(event_handler, folder_to_track, recursive=True)
observer.start()

try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
