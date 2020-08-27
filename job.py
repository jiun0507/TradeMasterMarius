from signal_handler import ProgramKilled
import threading
from time import time

class Job(threading.Thread):
    def __init__(self, interval, execute, *args, **kwargs):
        threading.Thread.__init__(self)
        self.daemon = False
        self.stopped = threading.Event()
        self.interval = interval
        self.execute = execute
        self.args = args
        self.kwargs = kwargs

    def stop(self):
                self.stopped.set()
                self.join()
    def run(self):
            while not self.stopped.wait(self.interval.total_seconds()):
                self.execute(*self.args, **self.kwargs)


class JobRunner:
    def __init__(self, jobs):
        self.jobs = jobs

    def run(self):
        for job in self.jobs:
            job.run()

        while True:
            try:
                time.sleep(1)
            except ProgramKilled:
                print("Program killed: running cleanup code")
                for job in self.jobs:
                    job.stop()
                break
