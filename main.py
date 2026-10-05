import tkinter as tk
from tkinter import messagebox, ttk
import pyperclip

from process import Process
from scheduler import ProcessQueue, FCFSScheduler, PriorityScheduler
from worker import ProcessWorker
from synchronization import Synchronization


# =========================================================
# Clipboard Manager
# =========================================================

class ClipboardManager:

    def __init__(self):

        self.history = []
        self.pinned = []
        self.last_clipboard = ""

    # -----------------------------------------------------
    # ตรวจสอบ Clipboard
    # -----------------------------------------------------

    def check_clipboard(self):

        try:

            current = pyperclip.paste()

            if not isinstance(current, str):
                return None

            current = current.strip()

            if not current:
                return None

            # Clipboard มีการเปลี่ยนแปลง
            if current != self.last_clipboard:

                self.last_clipboard = current

                # ไม่เพิ่ม History ซ้ำ
                if current not in self.history:

                    self.history.insert(
                        0,
                        current
                    )

                    return current

        except Exception as error:

            print(
                "Clipboard Error:",
                error
            )

        return None

    # -----------------------------------------------------
    # Copy กลับ Clipboard
    # -----------------------------------------------------

    def copy_text(self, text):

        pyperclip.copy(text)

        # ป้องกันไม่ให้โปรแกรมคิดว่า
        # Copy จากตัวโปรแกรมเองเป็น Clipboard ใหม่
        self.last_clipboard = text

    # -----------------------------------------------------
    # Delete
    # -----------------------------------------------------

    def delete_text(self, text):

        if text in self.history:

            self.history.remove(text)

        if text in self.pinned:

            self.pinned.remove(text)

    # -----------------------------------------------------
    # Pin / Unpin
    # -----------------------------------------------------

    def toggle_pin(self, text):

        if text in self.pinned:

            self.pinned.remove(text)

            return False

        self.pinned.append(text)

        return True


# =========================================================
# Main Application
# =========================================================

class ClipboardOSApp:

    def __init__(self, root):

        self.root = root

        # -------------------------------------------------
        # Window
        # -------------------------------------------------

        self.root.title(
            "Clipboard Manager OS"
        )

        self.root.geometry(
            "1150x820"
        )

        self.root.minsize(
            1000,
            700
        )

        # -------------------------------------------------
        # Clipboard Manager
        # -------------------------------------------------

        self.clipboard_manager = (
            ClipboardManager()
        )

        # -------------------------------------------------
        # OS Core
        # -------------------------------------------------

        self.process_queue = (
            ProcessQueue()
        )

        self.fcfs_scheduler = (
            FCFSScheduler()
        )

        self.priority_scheduler = (
            PriorityScheduler()
        )

        self.worker = (
            ProcessWorker()
        )

        self.sync = (
            Synchronization()
        )

        # -------------------------------------------------
        # Process Information
        # -------------------------------------------------

        self.pid_counter = 1

        self.all_processes = []

        self.completed_processes = []

        self.current_process = None

        self.scheduler_running = False

        # ใช้ map รายการ Listbox
        # กับข้อความจริง
        self.displayed_history = []

        # -------------------------------------------------
        # GUI
        # -------------------------------------------------

        self.create_gui()

        # -------------------------------------------------
        # เริ่ม Clipboard Monitoring
        # -------------------------------------------------

        self.monitor_clipboard()


    # =====================================================
    # GUI
    # =====================================================

    def create_gui(self):

        # =================================================
        # HEADER
        # =================================================

        header = tk.Frame(
            self.root,
            padx=20,
            pady=15
        )

        header.pack(
            fill="x"
        )

        title = tk.Label(
            header,
            text="Clipboard Manager OS",
            font=(
                "Arial",
                22,
                "bold"
            )
        )

        title.pack(
            side="left"
        )

        self.header_status = tk.Label(
            header,
            text="Monitoring Clipboard",
            font=(
                "Arial",
                10
            )
        )

        self.header_status.pack(
            side="right"
        )


        # =================================================
        # MAIN CONTAINER
        # =================================================

        main_container = tk.Frame(
            self.root
        )

        main_container.pack(
            fill="both",
            expand=True,
            padx=20
        )


        # =================================================
        # LEFT SIDE
        # Clipboard History
        # =================================================

        left_frame = tk.LabelFrame(
            main_container,
            text="Clipboard History",
            padx=10,
            pady=10
        )

        left_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(0, 10)
        )


        # -------------------------------------------------
        # Search
        # -------------------------------------------------

        search_frame = tk.Frame(
            left_frame
        )

        search_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            search_frame,
            text="Search:"
        ).pack(
            side="left"
        )

        self.search_entry = tk.Entry(
            search_frame
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True,
            padx=10
        )

        self.search_entry.bind(
            "<KeyRelease>",
            self.search_history
        )

        tk.Button(
            search_frame,
            text="Clear",
            command=self.clear_search
        ).pack(
            side="right"
        )


        # -------------------------------------------------
        # History List
        # -------------------------------------------------

        history_container = tk.Frame(
            left_frame
        )

        history_container.pack(
            fill="both",
            expand=True
        )

        history_scrollbar = tk.Scrollbar(
            history_container
        )

        history_scrollbar.pack(
            side="right",
            fill="y"
        )

        self.history_listbox = tk.Listbox(
            history_container,
            font=(
                "Arial",
                11
            ),
            yscrollcommand=(
                history_scrollbar.set
            )
        )

        self.history_listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        history_scrollbar.config(
            command=(
                self.history_listbox.yview
            )
        )


        # -------------------------------------------------
        # Clipboard Buttons
        # -------------------------------------------------

        clipboard_buttons = tk.Frame(
            left_frame
        )

        clipboard_buttons.pack(
            fill="x",
            pady=(10, 0)
        )

        tk.Button(
            clipboard_buttons,
            text="Copy",
            width=10,
            command=self.copy_selected
        ).pack(
            side="left",
            padx=3
        )

        tk.Button(
            clipboard_buttons,
            text="Pin / Unpin",
            width=12,
            command=self.pin_selected
        ).pack(
            side="left",
            padx=3
        )

        tk.Button(
            clipboard_buttons,
            text="Delete",
            width=10,
            command=self.delete_selected
        ).pack(
            side="left",
            padx=3
        )


        # =================================================
        # RIGHT SIDE
        # OS Process Manager
        # =================================================

        right_frame = tk.LabelFrame(
            main_container,
            text="OS Process Manager",
            padx=10,
            pady=10
        )

        right_frame.pack(
            side="right",
            fill="both",
            expand=True,
            padx=(10, 0)
        )


        # -------------------------------------------------
        # Scheduler Controls
        # -------------------------------------------------

        scheduler_frame = tk.Frame(
            right_frame
        )

        scheduler_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        tk.Label(
            scheduler_frame,
            text="Scheduling:"
        ).pack(
            side="left"
        )

        self.algorithm_var = (
            tk.StringVar(
                value="FCFS"
            )
        )

        self.algorithm_combo = (
            ttk.Combobox(
                scheduler_frame,
                textvariable=(
                    self.algorithm_var
                ),
                values=[
                    "FCFS",
                    "Priority"
                ],
                state="readonly",
                width=10
            )
        )

        self.algorithm_combo.pack(
            side="left",
            padx=8
        )

        # เมื่อเปลี่ยน Algorithm
        self.algorithm_combo.bind(
            "<<ComboboxSelected>>",
            self.algorithm_changed
        )


        # START
        tk.Button(
            scheduler_frame,
            text="START",
            width=9,
            command=self.start_scheduler
        ).pack(
            side="left",
            padx=2
        )


        # STOP
        tk.Button(
            scheduler_frame,
            text="STOP",
            width=9,
            command=self.stop_scheduler
        ).pack(
            side="left",
            padx=2
        )


        # CLEAR
        tk.Button(
            scheduler_frame,
            text="CLEAR",
            width=9,
            command=self.clear_queue
        ).pack(
            side="left",
            padx=2
        )


        # RESET DEMO
        tk.Button(
            scheduler_frame,
            text="RESET DEMO",
            width=12,
            command=self.reset_demo
        ).pack(
            side="left",
            padx=2
        )


        # -------------------------------------------------
        # Process Tree
        # -------------------------------------------------

        process_container = tk.Frame(
            right_frame
        )

        process_container.pack(
            fill="both",
            expand=True
        )

        columns = (
            "PID",
            "Content",
            "Priority",
            "State"
        )

        self.process_tree = ttk.Treeview(
            process_container,
            columns=columns,
            show="headings",
            height=15
        )


        # Column Headings

        self.process_tree.heading(
            "PID",
            text="PID"
        )

        self.process_tree.heading(
            "Content",
            text="Content"
        )

        self.process_tree.heading(
            "Priority",
            text="Priority"
        )

        self.process_tree.heading(
            "State",
            text="State"
        )


        # Column Size

        self.process_tree.column(
            "PID",
            width=55,
            anchor="center"
        )

        self.process_tree.column(
            "Content",
            width=190
        )

        self.process_tree.column(
            "Priority",
            width=80,
            anchor="center"
        )

        self.process_tree.column(
            "State",
            width=100,
            anchor="center"
        )


        # Scrollbar

        process_scrollbar = tk.Scrollbar(
            process_container,
            orient="vertical",
            command=(
                self.process_tree.yview
            )
        )

        self.process_tree.configure(
            yscrollcommand=(
                process_scrollbar.set
            )
        )

        self.process_tree.pack(
            side="left",
            fill="both",
            expand=True
        )

        process_scrollbar.pack(
            side="right",
            fill="y"
        )


        # -------------------------------------------------
        # Process State Colors
        # -------------------------------------------------

        self.process_tree.tag_configure(
            "READY",
            background="#fff4cc"
        )

        self.process_tree.tag_configure(
            "RUNNING",
            background="#d9edf7"
        )

        self.process_tree.tag_configure(
            "COMPLETED",
            background="#dff0d8"
        )


        # -------------------------------------------------
        # Priority Controls
        # -------------------------------------------------

        priority_frame = tk.Frame(
            right_frame
        )

        priority_frame.pack(
            fill="x",
            pady=(10, 0)
        )

        tk.Label(
            priority_frame,
            text="Set selected process:"
        ).pack(
            side="left"
        )

        tk.Button(
            priority_frame,
            text="HIGH",
            command=lambda:
            self.set_priority(
                "HIGH"
            )
        ).pack(
            side="left",
            padx=3
        )

        tk.Button(
            priority_frame,
            text="NORMAL",
            command=lambda:
            self.set_priority(
                "NORMAL"
            )
        ).pack(
            side="left",
            padx=3
        )

        tk.Button(
            priority_frame,
            text="LOW",
            command=lambda:
            self.set_priority(
                "LOW"
            )
        ).pack(
            side="left",
            padx=3
        )


        # =================================================
        # CPU / SCHEDULER STATUS
        # =================================================

        cpu_frame = tk.LabelFrame(
            self.root,
            text="CPU / Scheduler Status",
            padx=15,
            pady=10
        )

        cpu_frame.pack(
            fill="x",
            padx=20,
            pady=(10, 0)
        )


        # Current Process

        self.current_process_label = (
            tk.Label(
                cpu_frame,
                text=(
                    "Current Process: IDLE"
                ),
                font=(
                    "Arial",
                    11,
                    "bold"
                )
            )
        )

        self.current_process_label.pack(
            side="left",
            padx=15
        )


        # Algorithm

        self.current_algorithm_label = (
            tk.Label(
                cpu_frame,
                text="Algorithm: FCFS",
                font=(
                    "Arial",
                    11
                )
            )
        )

        self.current_algorithm_label.pack(
            side="left",
            padx=30
        )


        # CPU State

        self.cpu_state_label = tk.Label(
            cpu_frame,
            text="CPU State: IDLE",
            font=(
                "Arial",
                11
            )
        )

        self.cpu_state_label.pack(
            side="left",
            padx=30
        )


        # =================================================
        # STATISTICS
        # =================================================

        statistics_frame = tk.LabelFrame(
            self.root,
            text="Statistics",
            padx=15,
            pady=10
        )

        statistics_frame.pack(
            fill="x",
            padx=20,
            pady=10
        )


        # Total Processes

        self.total_label = tk.Label(
            statistics_frame,
            text="Total Processes: 0"
        )

        self.total_label.pack(
            side="left",
            padx=12
        )


        # Queue

        self.queue_label = tk.Label(
            statistics_frame,
            text="Queue: 0"
        )

        self.queue_label.pack(
            side="left",
            padx=12
        )


        # Completed

        self.completed_label = tk.Label(
            statistics_frame,
            text="Completed: 0"
        )

        self.completed_label.pack(
            side="left",
            padx=12
        )


        # Average Waiting

        self.waiting_label = tk.Label(
            statistics_frame,
            text="Avg Waiting: 0.00s"
        )

        self.waiting_label.pack(
            side="left",
            padx=12
        )


        # Average Turnaround

        self.turnaround_label = tk.Label(
            statistics_frame,
            text=(
                "Avg Turnaround: 0.00s"
            )
        )

        self.turnaround_label.pack(
            side="left",
            padx=12
        )


        # =================================================
        # BOTTOM STATUS BAR
        # =================================================

        self.status_label = tk.Label(
            self.root,
            text="Ready",
            anchor="w",
            relief="sunken",
            padx=10
        )

        self.status_label.pack(
            fill="x",
            side="bottom"
        )


    # =====================================================
    # Clipboard Monitoring
    # =====================================================

    def monitor_clipboard(self):

        new_text = (
            self.clipboard_manager
            .check_clipboard()
        )

        if new_text:

            # Update Clipboard History
            self.update_history()

            # สร้าง Process ใหม่
            self.create_process(
                new_text
            )

            self.status_label.config(
                text=(
                    "New clipboard item detected "
                    "and added to Process Queue."
                )
            )

        # ตรวจ Clipboard ทุก 500 ms
        self.root.after(
            500,
            self.monitor_clipboard
        )


    # =====================================================
    # Clipboard History
    # =====================================================

    def update_history(self):

        keyword = (
            self.search_entry
            .get()
            .lower()
        )

        self.history_listbox.delete(
            0,
            tk.END
        )

        self.displayed_history = []

        for item in (
            self.clipboard_manager.history
        ):

            if (
                keyword
                and keyword
                not in item.lower()
            ):

                continue

            self.displayed_history.append(
                item
            )

            preview = item.replace(
                "\n",
                " "
            )

            if len(preview) > 70:

                preview = (
                    preview[:70]
                    + "..."
                )

            if item in (
                self.clipboard_manager
                .pinned
            ):

                preview = (
                    "[PIN] "
                    + preview
                )

            self.history_listbox.insert(
                tk.END,
                preview
            )


    # -----------------------------------------------------
    # Get Selected Clipboard Item
    # -----------------------------------------------------

    def get_selected_history_text(self):

        selection = (
            self.history_listbox
            .curselection()
        )

        if not selection:

            messagebox.showwarning(
                "Warning",
                "Please select a clipboard item."
            )

            return None

        index = selection[0]

        if index >= len(
            self.displayed_history
        ):

            return None

        return (
            self.displayed_history[
                index
            ]
        )


    # -----------------------------------------------------
    # Copy
    # -----------------------------------------------------

    def copy_selected(self):

        text = (
            self.get_selected_history_text()
        )

        if text is None:
            return

        self.clipboard_manager.copy_text(
            text
        )

        self.status_label.config(
            text=(
                "Selected item copied "
                "to Clipboard."
            )
        )


    # -----------------------------------------------------
    # Delete
    # -----------------------------------------------------

    def delete_selected(self):

        text = (
            self.get_selected_history_text()
        )

        if text is None:
            return

        self.clipboard_manager.delete_text(
            text
        )

        self.update_history()

        self.status_label.config(
            text=(
                "Clipboard history "
                "item deleted."
            )
        )


    # -----------------------------------------------------
    # Pin / Unpin
    # -----------------------------------------------------

    def pin_selected(self):

        text = (
            self.get_selected_history_text()
        )

        if text is None:
            return

        pinned = (
            self.clipboard_manager
            .toggle_pin(text)
        )

        self.update_history()

        if pinned:

            self.status_label.config(
                text=(
                    "Clipboard item pinned."
                )
            )

        else:

            self.status_label.config(
                text=(
                    "Clipboard item unpinned."
                )
            )


    # -----------------------------------------------------
    # Search
    # -----------------------------------------------------

    def search_history(
        self,
        event=None
    ):

        self.update_history()


    # -----------------------------------------------------
    # Clear Search
    # -----------------------------------------------------

    def clear_search(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.update_history()


    # =====================================================
    # Create Process
    # =====================================================

    def create_process(
        self,
        content
    ):

        pid = (
            f"P{self.pid_counter}"
        )

        self.pid_counter += 1

        process = Process(
            pid,
            content,
            "NORMAL"
        )

        # ---------------------------------------------
        # Critical Section
        # ---------------------------------------------

        self.sync.acquire()

        try:

            self.process_queue.add(
                process
            )

            self.all_processes.append(
                process
            )

        finally:

            self.sync.release()

        self.update_process_tree()

        self.update_statistics()


    # =====================================================
    # Set Priority
    # =====================================================

    def set_priority(
        self,
        priority
    ):

        selected = (
            self.process_tree
            .selection()
        )

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select a process."
            )

            return

        item = selected[0]

        values = (
            self.process_tree
            .item(
                item,
                "values"
            )
        )

        pid = values[0]

        for process in (
            self.all_processes
        ):

            if (
                process.pid == pid
                and
                process.state
                == "READY"
            ):

                process.priority = (
                    priority
                )

                self.status_label.config(
                    text=(
                        f"{pid} priority "
                        f"changed to "
                        f"{priority}."
                    )
                )

                self.update_process_tree()

                return

        messagebox.showinfo(
            "Priority",
            (
                "Priority can only "
                "be changed while "
                "the process is READY."
            )
        )


    # =====================================================
    # Algorithm Changed
    # =====================================================

    def algorithm_changed(
        self,
        event=None
    ):

        algorithm = (
            self.algorithm_var.get()
        )

        self.current_algorithm_label.config(
            text=(
                f"Algorithm: "
                f"{algorithm}"
            )
        )

        self.status_label.config(
            text=(
                "Scheduling algorithm "
                f"changed to {algorithm}."
            )
        )


    # =====================================================
    # Start Scheduler
    # =====================================================

    def start_scheduler(self):

        if self.scheduler_running:

            return

        if self.process_queue.is_empty():

            messagebox.showinfo(
                "Process Queue",
                "The Process Queue is empty."
            )

            return

        self.scheduler_running = True

        algorithm = (
            self.algorithm_var.get()
        )

        self.current_algorithm_label.config(
            text=(
                f"Algorithm: "
                f"{algorithm}"
            )
        )

        self.status_label.config(
            text=(
                f"{algorithm} "
                "Scheduler started."
            )
        )

        self.run_next_process()


    # =====================================================
    # Stop Scheduler
    # =====================================================

    def stop_scheduler(self):

        self.scheduler_running = False

        self.status_label.config(
            text=(
                "Scheduler stopped. "
                "Current process will "
                "finish normally."
            )
        )


    # =====================================================
    # Run Next Process
    # =====================================================

    def run_next_process(self):

        if not self.scheduler_running:

            return

        # Worker ยังทำงานอยู่
        if self.worker.running:

            return

        selected = None

        # ---------------------------------------------
        # Critical Section
        # ---------------------------------------------

        self.sync.acquire()

        try:

            processes = (
                self.process_queue
                .get_all()
            )

            # ไม่มี Process เหลือ
            if not processes:

                self.scheduler_running = False

                self.current_process = None

            else:

                algorithm = (
                    self.algorithm_var
                    .get()
                )

                # Priority Scheduling
                if algorithm == "Priority":

                    selected = (
                        self.priority_scheduler
                        .select_process(
                            processes
                        )
                    )

                # FCFS
                else:

                    selected = (
                        self.fcfs_scheduler
                        .select_process(
                            processes
                        )
                    )

                if selected is not None:

                    # เอาออกจาก Waiting Queue
                    self.process_queue.remove(
                        selected
                    )

                    self.current_process = (
                        selected
                    )

        finally:

            self.sync.release()


        # ---------------------------------------------
        # Queue เสร็จทั้งหมด
        # ---------------------------------------------

        if selected is None:

            self.current_process_label.config(
                text=(
                    "Current Process: IDLE"
                )
            )

            self.cpu_state_label.config(
                text="CPU State: IDLE"
            )

            self.status_label.config(
                text=(
                    "All queued processes "
                    "completed."
                )
            )

            self.update_process_tree()

            self.update_statistics()

            return


        # ---------------------------------------------
        # Worker จะเป็นผู้เปลี่ยน
        # READY -> RUNNING
        # ---------------------------------------------

        self.current_process_label.config(
            text=(
                f"Current Process: "
                f"{selected.pid}"
            )
        )

        self.cpu_state_label.config(
            text="CPU State: RUNNING"
        )

        self.current_algorithm_label.config(
            text=(
                "Algorithm: "
                f"{self.algorithm_var.get()}"
            )
        )

        self.status_label.config(
            text=(
                f"{selected.pid} "
                "is running..."
            )
        )

        # ให้ Worker จัดการ Thread
        self.worker.execute(
            selected,
            self.worker_finished
        )

        # Worker เปลี่ยน State
        # ใน Thread จึง refresh หลังเล็กน้อย
        self.root.after(
            50,
            self.update_process_tree
        )

        self.root.after(
            50,
            self.update_statistics
        )


    # =====================================================
    # Worker Callback
    # =====================================================

    def worker_finished(
        self,
        process
    ):

        # Callback มาจาก Worker Thread
        # ห้าม Update Tkinter โดยตรง
        # ต้องส่งกลับ Main Thread

        self.root.after(
            0,
            lambda:
            self.finish_process(
                process
            )
        )


    # =====================================================
    # Finish Process
    # =====================================================

    def finish_process(
        self,
        process
    ):

        if process not in (
            self.completed_processes
        ):

            self.completed_processes.append(
                process
            )

        self.current_process = None

        # CPU กลับ IDLE ชั่วคราว
        self.current_process_label.config(
            text=(
                "Current Process: IDLE"
            )
        )

        self.cpu_state_label.config(
            text="CPU State: IDLE"
        )

        self.update_process_tree()

        self.update_statistics()

        self.status_label.config(
            text=(
                f"{process.pid} "
                "completed."
            )
        )

        # ถ้า Scheduler ยังทำงาน
        # ให้ Process ตัวต่อไปทำงาน
        if self.scheduler_running:

            self.root.after(
                300,
                self.run_next_process
            )


    # =====================================================
    # Clear Queue
    # =====================================================

    def clear_queue(self):

        # ห้าม Clear ตอน Process กำลังทำงาน
        if self.worker.running:

            messagebox.showwarning(
                "Process Running",
                (
                    "Cannot clear the queue "
                    "while a process is running."
                )
            )

            return

        self.scheduler_running = False

        self.sync.acquire()

        try:

            queued_processes = (
                self.process_queue
                .get_all()
            )

            self.process_queue.clear()

            # เอาเฉพาะ Process ที่ยังรอ
            # ออกจาก Process List
            for process in queued_processes:

                if process in (
                    self.all_processes
                ):

                    self.all_processes.remove(
                        process
                    )

        finally:

            self.sync.release()

        self.current_process = None

        self.current_process_label.config(
            text="Current Process: IDLE"
        )

        self.cpu_state_label.config(
            text="CPU State: IDLE"
        )

        self.update_process_tree()

        self.update_statistics()

        self.status_label.config(
            text=(
                "Process Queue cleared."
            )
        )


    # =====================================================
    # Reset Demo
    # =====================================================

    def reset_demo(self):

        # ---------------------------------------------
        # ห้าม Reset ขณะ Worker ทำงาน
        # ---------------------------------------------

        if self.worker.running:

            messagebox.showwarning(
                "Process Running",
                (
                    "Please wait until the "
                    "current process finishes "
                    "before resetting."
                )
            )

            return


        # ---------------------------------------------
        # Confirm
        # ---------------------------------------------

        confirm = (
            messagebox.askyesno(
                "Reset Demo",
                (
                    "Reset all processes "
                    "and statistics?\n\n"
                    "Clipboard History "
                    "will be kept."
                )
            )
        )

        if not confirm:

            return


        # ---------------------------------------------
        # Stop Scheduler
        # ---------------------------------------------

        self.scheduler_running = False


        # ---------------------------------------------
        # Critical Section
        # ---------------------------------------------

        self.sync.acquire()

        try:

            self.process_queue.clear()

            self.all_processes.clear()

            self.completed_processes.clear()

        finally:

            self.sync.release()


        # ---------------------------------------------
        # Reset Process Information
        # ---------------------------------------------

        self.pid_counter = 1

        self.current_process = None


        # ---------------------------------------------
        # Reset GUI
        # ---------------------------------------------

        self.current_process_label.config(
            text=(
                "Current Process: IDLE"
            )
        )

        self.cpu_state_label.config(
            text="CPU State: IDLE"
        )

        self.current_algorithm_label.config(
            text=(
                "Algorithm: "
                f"{self.algorithm_var.get()}"
            )
        )

        self.update_process_tree()

        self.update_statistics()

        self.status_label.config(
            text=(
                "Demo reset completed. "
                "Clipboard History was kept."
            )
        )


    # =====================================================
    # Update Process Tree
    # =====================================================

    def update_process_tree(self):

        # ลบข้อมูลเก่า
        for item in (
            self.process_tree
            .get_children()
        ):

            self.process_tree.delete(
                item
            )


        # ใส่ข้อมูลใหม่
        for process in (
            self.all_processes
        ):

            preview = (
                process.content
                .replace(
                    "\n",
                    " "
                )
            )

            if len(preview) > 30:

                preview = (
                    preview[:30]
                    + "..."
                )

            self.process_tree.insert(
                "",
                tk.END,
                values=(
                    process.pid,
                    preview,
                    process.priority,
                    process.state
                ),

                # สีตาม Process State
                tags=(
                    process.state,
                )
            )


    # =====================================================
    # Update Statistics
    # =====================================================

    def update_statistics(self):

        total = len(
            self.all_processes
        )

        queue_size = (
            self.process_queue.size()
        )

        completed = len(
            self.completed_processes
        )


        # ---------------------------------------------
        # Average Time
        # ---------------------------------------------

        if completed > 0:

            total_waiting = sum(
                process.waiting_time
                for process
                in self.completed_processes
            )

            total_turnaround = sum(
                process.turnaround_time
                for process
                in self.completed_processes
            )

            average_waiting = (
                total_waiting
                / completed
            )

            average_turnaround = (
                total_turnaround
                / completed
            )

        else:

            average_waiting = 0

            average_turnaround = 0


        # ---------------------------------------------
        # Update Labels
        # ---------------------------------------------

        self.total_label.config(
            text=(
                f"Total Processes: "
                f"{total}"
            )
        )

        self.queue_label.config(
            text=(
                f"Queue: "
                f"{queue_size}"
            )
        )

        self.completed_label.config(
            text=(
                f"Completed: "
                f"{completed}"
            )
        )

        self.waiting_label.config(
            text=(
                "Avg Waiting: "
                f"{average_waiting:.2f}s"
            )
        )

        self.turnaround_label.config(
            text=(
                "Avg Turnaround: "
                f"{average_turnaround:.2f}s"
            )
        )


# =========================================================
# Start Application
# =========================================================

if __name__ == "__main__":

    root = tk.Tk()

    app = ClipboardOSApp(
        root
    )

    root.mainloop()