import threading
import time


class ProcessWorker:

    def __init__(self):

        self.thread = None

        self.running = False

    def execute(self, process, on_complete=None):

        self.thread = threading.Thread(
            target=self._run_process,
            args=(process, on_complete),
            daemon=True
        )

        self.thread.start()

    def _run_process(
        self,
        process,
        on_complete
    ):

        self.running = True

        # READY → RUNNING
        process.start()

        print(
            f"{process.pid} is running..."
        )

        # จำลองการประมวลผล
        time.sleep(2)

        # RUNNING → COMPLETED
        process.complete()

        print(
            f"{process.pid} completed."
        )

        self.running = False

        # แจ้งกลับเมื่อเสร็จ
        if on_complete:

            on_complete(process)