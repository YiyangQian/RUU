import numpy as np
import math

class Parser(object):
    '''
    {time_minute : {process_created: 0, process_deleted: 0, 
                     window_top: 0, window_leave: 0, 
                     file_modified: 0, file_created: 0, file_deleted: 0,  
                     directory_created: 0, directory_deleted: 0}}
    '''
    frequency = {}
    def __init__(self):
        self.frequency = {}

    def parse_process(self, process_log_path):
        lines = []
        log = open(process_log_path)
        try:
            lines = log.read().splitlines()
        finally:
            log.close()
        for line in lines:
            time, action_type, action, exe = line.split(", ")
            time_minute = time[:-3]
            if time_minute not in self.frequency: 
                self.frequency[time_minute] = {"process_created": 0, "process_deleted": 0, 
                                                "window_top": 0, "window_leave": 0, 
                                                "file_modified": 0, "file_created": 0, "file_deleted": 0,  
                                                "directory_created": 0, "directory_deleted": 0}
            cur = self.frequency[time_minute]
            if action == "create":
                cur["process_created"] += 1
            else:
                cur["process_deleted"] += 1
    
    def parse_window(self, window_log_path):
        lines = []
        log = open(window_log_path)
        try:
            lines = log.read().splitlines()
        finally:
            log.close()
        for line in lines:
            time, action_type, action, exe = line.split(", ")
            time_minute = time[:-3]
            if time_minute not in self.frequency: 
                self.frequency[time_minute] = {"process_created": 0, "process_deleted": 0, 
                                                "window_top": 0, "window_leave": 0, 
                                                "file_modified": 0, "file_created": 0, "file_deleted": 0,  
                                                "directory_created": 0, "directory_deleted": 0}
            cur = self.frequency[time_minute]
            if action == "top":
                cur["window_top"] += 1
            else:
                cur["window_leave"] += 1
    
    def parse_file(self, file_log_path):
        lines = []
        log = open(file_log_path)
        try:
            lines = log.read().splitlines()
        finally:
            log.close()
        for line in lines:
            time, action_type, action, exe = line.split(", ")
            time_minute = time[:-3]
            if time_minute not in self.frequency: 
                self.frequency[time_minute] = {"process_created": 0, "process_deleted": 0, 
                                                "window_top": 0, "window_leave": 0, 
                                                "file_modified": 0, "file_created": 0, "file_deleted": 0,  
                                                "directory_created": 0, "directory_deleted": 0}
            cur = self.frequency[time_minute]
            if action_type == "file":
                if action == "modified":
                    cur["file_modified"] += 1
                elif action == "created":
                    cur["file_created"] += 1
                else:
                    cur["file_deleted"] += 1
            else:
                if action == "created":
                    cur["directory_created"] += 1
                else:
                    cur["directory_deleted"] += 1

    def generateNpArray(self):
        store = []
        for key, value in self.frequency.iteritems():
            store.append([math.log(value['process_created'] + 1), math.log(value["process_deleted"] + 1), 
                        math.log(value["window_top"] + 1), math.log(value["window_leave"] + 1),
                        math.log(value["file_modified"] + 1), math.log(value["file_created"] + 1), math.log(value["file_deleted"] + 1),
                        math.log(value["directory_created"] + 1), math.log(value["directory_deleted"] + 1)])
        arr = np.array(store)
        return arr
    
    def parse(self, process_log_path, window_log_path, file_log_path):
        self.parse_process(process_log_path)
        self.parse_window(window_log_path)
        self.parse_file(file_log_path)
        return self.generateNpArray()
