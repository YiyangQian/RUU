import sys
import time
import logging
from watchdog import *
from watchdog.observers import Observer
from watchdog.events import *
from datetime import datetime

class CustomFileEventHandler(PatternMatchingEventHandler):
    path_to_write = ""

    def __init__(self, path_to_write):
        super(CustomFileEventHandler, self).__init__(ignore_patterns=['*/*_log.txt'])
        self.path_to_write = path_to_write

    def on_any_event(self, event):
        file_name = event.src_path
        with open(self.path_to_write, "a") as log_file:
            what = 'directory' if event.is_directory else "file"
            if isinstance(event, FileModifiedEvent):
                modified = (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), what, 'modified', file_name)
                log_file.write("{}, {}, {}, {}".format(modified[0], modified[1], modified[2], modified[3]))
                log_file.write('\n')
            elif isinstance(event, DirCreatedEvent) or isinstance(event, FileCreatedEvent):
                created = ((datetime.now().strftime('%Y-%m-%d %H:%M:%S'), what, 'created', file_name))
                log_file.write("{}, {}, {}, {}".format(created[0], created[1], created[2], created[3]))
                log_file.write('\n')
            elif isinstance(event, FileDeletedEvent) or isinstance(event, DirDeletedEvent):
                deleted = ((datetime.now().strftime('%Y-%m-%d %H:%M:%S'), what, 'deleted', file_name))
                log_file.write("{}, {}, {}, {}".format(deleted[0], deleted[1], deleted[2], deleted[3]))
                log_file.write('\n')
            else:
                pass
            
class FileSensor(object):
    path = "."
    path_to_write = ""
    
    def __init__(self, path_to_monitor, path_to_write):
        self.path = path_to_monitor
        self.path_to_write = path_to_write

    def monitor(self):
        event_handler = CustomFileEventHandler(self.path_to_write)
        observer = Observer()
        observer.schedule(event_handler, self.path, recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    
if __name__ == "__main__":
    path = '/Users/yiyang/Documents/'
    fs = FileSensor(path, "stranger2_file_log.txt")
    fs.monitor()
