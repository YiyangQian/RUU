import psutil
from datetime import datetime
import time

class ProcessSensor(object): 
    # process ID, executable path, state, time, parent process ID
    past_list = []
    store = {}
    seconds = 0
    iterations = 0
    interval_seconds = 0

    def __init__(self, days, interval_seconds):
        self.past_list = psutil.pids()
        self.update_store()
        self.seconds = days * 24 * 60 * 60
        self.interval_seconds = interval_seconds
        self.iterations = self.seconds / interval_seconds

    def get_added_pid(self, cur_list):
        added = []
        for pid in cur_list:
            if pid not in self.past_list:
                added.append(pid)
        return added

    def get_removed_pid(self, cur_list):
        removed = []
        for pid in self.past_list:
            if pid not in cur_list:
                removed.append(pid)
        return removed 

    def update_store(self):
        for p in psutil.process_iter(attrs=['pid', 'exe', 'create_time', 'ppid']):
            # p is instance of psutil.Process, p.info is a dict
            # sample {'ppid': 1, 'create_time': 1541565218.222305, 'pid': 2093, 'exe': '/usr/sample/test'}
            pid = p.info['pid']
            p.info.pop('pid')
            self.store[pid] = p.info
    
    def getCurList(self):
        return psutil.pids()
    
    def updateListsAndStore(self):
        cur_list = self.getCurList()
        added = self.get_added_pid(cur_list)
        removed = self.get_removed_pid(cur_list)
        self.update_store()
        self.past_list = cur_list
        return added, removed
    
    def getTime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def generateLogTuples(self, pids, isCreate):
        res = []
        action = ""
        if isCreate:
            action = "create"
        else:
            action = "delete"
        for pid in pids:
            if pid in self.store:
                curLog = (self.getTime(), "process", action, self.store[pid]['exe'])
                res.append(curLog)
        return res

    def monitor(self):
        for i in range(self.iterations):
            time.sleep(self.interval_seconds)
            added, removed = self.updateListsAndStore()
            addedLogs = self.generateLogTuples(added, True)
            removedLogs = self.generateLogTuples(removed, False)
            logs = addedLogs + removedLogs
            if len(logs) != 0:
                with open("process_log.txt", 'a') as log_file:
                    log_file.write('\n'.join('{}, {}, {}, {}'.format(log[0], log[1], log[2], log[3]) for log in logs))
                    log_file.write('\n')

if __name__ == "__main__":
    ps = ProcessSensor(4, 10)
    ps.monitor()
