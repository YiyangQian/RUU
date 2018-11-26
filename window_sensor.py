import sys
from AppKit import NSWorkspace
import time
from datetime import datetime

class WindowSensor(object):
    front_most_app = ""
    seconds = 0
    iterations = 0
    interval_seconds = 0

    def __init__(self, days, interval_seconds):
        self.seconds = days * 24 * 60 * 60
        self.interval_seconds = interval_seconds
        self.iterations = self.seconds / self.interval_seconds
        self.front_most_app = self.getFrontMostApplication()
    
    def getFrontMostApplication(self):
        '''
        sample out put of NSWorkspace.sharedWorkspace().activeApplication()
        {
            NSApplicationBundleIdentifier = "com.microsoft.VSCode";
            NSApplicationName = Code;
            NSApplicationPath = "/Applications/Visual Studio Code.app";
            NSApplicationProcessIdentifier = 384;
            NSApplicationProcessSerialNumberHigh = 0;
            NSApplicationProcessSerialNumberLow = 114716;
            NSWorkspaceApplicationKey = "<NSRunningApplication: 0x7feb92594fb0 (com.microsoft.VSCode - 384)>";
        }
        '''
        return NSWorkspace.sharedWorkspace().activeApplication()["NSApplicationName"]
    
    def getTime(self):
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def monitor(self):
        for i in range(self.iterations):
            time.sleep(self.interval_seconds)
            cur_time = self.getTime()
            cur_front_most_app = self.getFrontMostApplication()
            if cur_front_most_app != self.front_most_app:
                topped = (cur_time, "window", "top", cur_front_most_app)
                left = (cur_time, "window", "leave", self.front_most_app)
                self.front_most_app = cur_front_most_app
                with open("window_log.txt", 'a') as log_file:
                    log_file.write('{}, {}, {}, {}'.format(topped[0], topped[1], topped[2], topped[3]))
                    log_file.write('\n') 
                    log_file.write('{}, {}, {}, {}'.format(left[0], left[1], left[2], left[3]))
                    log_file.write('\n')

if __name__ == "__main__":
    ws = WindowSensor(4, 10)
    ws.monitor()