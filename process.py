import time


class Process:

    def __init__(self, pid, content, priority="NORMAL"):

        self.pid = pid
        self.content = content
        self.priority = priority

        # Process State
        self.state = "READY"

        # Time information
        self.created_time = time.time()
        self.start_time = None
        self.finish_time = None

        # Statistics
        self.waiting_time = 0
        self.turnaround_time = 0

    def start(self):

        self.state = "RUNNING"

        self.start_time = time.time()

        # Waiting Time
        self.waiting_time = (
            self.start_time - self.created_time
        )

    def complete(self):

        self.state = "COMPLETED"

        self.finish_time = time.time()

        # Turnaround Time
        self.turnaround_time = (
            self.finish_time - self.created_time
        )

    def __str__(self):

        return (
            f"{self.pid} | "
            f"{self.content} | "
            f"{self.priority} | "
            f"{self.state}"
        )