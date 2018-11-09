import psutil 

class ProcessSensor: 
    # process ID, executable path, state, time, parent process ID
    past_store = {}
    past_list = []

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

    def generate_store(self):
        cur_store = {}
        for p in psutil.process_iter(attrs=['pid', 'exe', 'create_time', 'ppid']):
            # p is instance of psutil.Process, p.info is a dict
            # sample {'ppid': 1, 'create_time': 1541565218.222305, 'pid': 2093, 'exe': '/usr/sample/test'}
            pid = p.info['pid']
            p.info.pop('pid')
            cur_store[pid] = p.info
        return cur_store 

    def generate_log(self, interval):
        pass
