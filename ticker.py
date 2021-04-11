import time
from threading import Thread


class Ticker:
    def __init__(self, processes):
        self.is_running = True
        self.processes = processes
        self.thread = None

    def start(self):
        self.thread = Thread(target=self.__tick)
        self.thread.start()

    def stop(self):
        self.is_running = False
        if self.thread is not None:
            self.thread.join()

    def upd_list(self, new_processes):
        self.processes = new_processes

    # approx clock
    def __tick(self):
        t = 0
        interval = 1  # s
        threshold = 5  # every 5 seconds go up a minute?

        while self.is_running:
            time.sleep(interval)
            t += interval
            if t >= threshold:
                t = 0
                for p in self.processes:
                    p.tick()
