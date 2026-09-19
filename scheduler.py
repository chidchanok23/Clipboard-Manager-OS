from collections import deque


class ProcessQueue:

    def __init__(self):

        self.queue = deque()

    def add(self, process):

        self.queue.append(process)

    def get_all(self):

        return list(self.queue)

    def remove(self, process):

        if process in self.queue:

            self.queue.remove(process)

    def clear(self):

        self.queue.clear()

    def is_empty(self):

        return len(self.queue) == 0

    def size(self):

        return len(self.queue)


class FCFSScheduler:

    def select_process(self, processes):

        if not processes:

            return None

        # First Come First Serve
        return processes[0]


class PriorityScheduler:

    priority_value = {

        "HIGH": 1,
        "NORMAL": 2,
        "LOW": 3

    }

    def select_process(self, processes):

        if not processes:

            return None

        # เลือก Priority สูงสุดก่อน
        return min(
            processes,
            key=lambda process:
            self.priority_value[
                process.priority
            ]
        )