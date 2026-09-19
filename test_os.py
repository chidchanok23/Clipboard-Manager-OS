from process import Process
from scheduler import (
    ProcessQueue,
    FCFSScheduler,
    PriorityScheduler
)
from synchronization import Synchronization
from worker import ProcessWorker

import time


# ========================================
# 1. สร้าง Process
# ========================================

p1 = Process(
    "P1",
    "Operating Systems",
    "NORMAL"
)

p2 = Process(
    "P2",
    "CP353002",
    "HIGH"
)

p3 = Process(
    "P3",
    "Hello World",
    "LOW"
)


print("=== PROCESS ===")

print(p1)
print(p2)
print(p3)


# ========================================
# 2. Process Queue
# ========================================

queue = ProcessQueue()

queue.add(p1)
queue.add(p2)
queue.add(p3)


print("\n=== QUEUE ===")

for process in queue.get_all():

    print(process)


# ========================================
# 3. FCFS
# ========================================

fcfs = FCFSScheduler()

selected = fcfs.select_process(
    queue.get_all()
)

print("\n=== FCFS ===")

print(
    "Selected:",
    selected
)


# ========================================
# 4. Priority
# ========================================

priority = PriorityScheduler()

selected = priority.select_process(
    queue.get_all()
)

print("\n=== PRIORITY ===")

print(
    "Selected:",
    selected
)


# ========================================
# 5. Synchronization
# ========================================

sync = Synchronization()

print("\n=== LOCK ===")

print(
    "Locked:",
    sync.locked()
)

sync.acquire()

print(
    "Locked after acquire:",
    sync.locked()
)

sync.release()

print(
    "Locked after release:",
    sync.locked()
)


# ========================================
# 6. Worker Thread
# ========================================

worker = ProcessWorker()


print("\n=== WORKER ===")

worker.execute(
    p1
)

# รอให้ Thread ทำงานเสร็จ
time.sleep(3)

print(
    "Final State:",
    p1.state
)

print(
    "Waiting Time:",
    round(
        p1.waiting_time,
        2
    ),
    "seconds"
)

print(
    "Turnaround Time:",
    round(
        p1.turnaround_time,
        2
    ),
    "seconds"
)