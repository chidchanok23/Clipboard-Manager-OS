import threading


class Synchronization:

    def __init__(self):

        self.lock = threading.Lock()

    def acquire(self):

        self.lock.acquire()

    def release(self):

        self.lock.release()

    def locked(self):

        return self.lock.locked()