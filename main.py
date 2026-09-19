import tkinter as tk
from tkinter import messagebox
import pyperclip


class ClipboardManager:

    def __init__(self):
        # เก็บประวัติ Clipboard
        self.history = []

        # เก็บรายการที่ Pin
        self.pinned = []

        # Clipboard ล่าสุดที่ตรวจพบ
        self.last_clipboard = ""

    # ========================================
    # STEP 6: ตรวจสอบ Clipboard
    # ========================================

    def check_clipboard(self):

        try:
            current = pyperclip.paste()

            # ถ้ามีข้อความใหม่
            if current and current != self.last_clipboard:

                self.last_clipboard = current

                # ไม่เพิ่มข้อมูลซ้ำ
                if current not in self.history:

                    # เพิ่มข้อมูลใหม่ไว้ด้านบน
                    self.history.insert(0, current)

        except Exception:
            pass

    # ========================================
    # STEP 7: Copy กลับไป Clipboard
    # ========================================

    def copy_item(self, index):

        if 0 <= index < len(self.history):

            text = self.history[index]

            pyperclip.copy(text)

            return True

        return False

    # ========================================
    # STEP 8: Delete
    # ========================================

    def delete_item(self, index):

        if 0 <= index < len(self.history):

            text = self.history[index]

            # ลบจาก History
            self.history.pop(index)

            # ถ้าอยู่ใน Pinned ด้วย ให้ลบออก
            if text in self.pinned:
                self.pinned.remove(text)

            return True

        return False

    # ========================================
    # STEP 9: Pin
    # ========================================

    def pin_item(self, index):

        if 0 <= index < len(self.history):

            text = self.history[index]

            if text not in self.pinned:

                self.pinned.append(text)

                return True

        return False


class App:

    def __init__(self, root):

        self.root = root

        # ========================================
        # หน้าต่างหลัก
        # ========================================

        self.root.title("Clipboard Manager OS")

        self.root.geometry("900x650")

        self.root.minsize(800, 550)

        # ========================================
        # Clipboard Manager
        # ========================================

        self.manager = ClipboardManager()

        # ========================================
        # Title
        # ========================================

        title = tk.Label(
            root,
            text="📋 Clipboard Manager OS",
            font=("Arial", 22, "bold")
        )

        title.pack(pady=(20, 5))

        subtitle = tk.Label(
            root,
            text="Clipboard History Manager",
            font=("Arial", 11)
        )

        subtitle.pack(pady=(0, 15))

        # ========================================
        # STEP 10: Search
        # ========================================

        search_frame = tk.Frame(root)

        search_frame.pack(
            fill="x",
            padx=30,
            pady=5
        )

        search_label = tk.Label(
            search_frame,
            text="🔍 Search:"
        )

        search_label.pack(
            side="left",
            padx=(0, 10)
        )

        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 11)
        )

        self.search_entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        # ตรวจสอบทุกครั้งที่พิมพ์
        self.search_entry.bind(
            "<KeyRelease>",
            self.search
        )

        # ========================================
        # History Label
        # ========================================

        history_label = tk.Label(
            root,
            text="Clipboard History",
            font=("Arial", 14, "bold")
        )

        history_label.pack(
            anchor="w",
            padx=30,
            pady=(15, 5)
        )

        # ========================================
        # Listbox
        # ========================================

        list_frame = tk.Frame(root)

        list_frame.pack(
            fill="both",
            expand=True,
            padx=30
        )

        scrollbar = tk.Scrollbar(
            list_frame
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        self.listbox = tk.Listbox(
            list_frame,
            width=90,
            height=18,
            font=("Arial", 11),
            yscrollcommand=scrollbar.set
        )

        self.listbox.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(
            command=self.listbox.yview
        )

        # ========================================
        # Buttons
        # ========================================

        button_frame = tk.Frame(root)

        button_frame.pack(
            pady=15
        )

        # Copy
        self.copy_button = tk.Button(
            button_frame,
            text="📋 Copy",
            width=12,
            command=self.copy_selected
        )

        self.copy_button.pack(
            side="left",
            padx=5
        )

        # Pin
        self.pin_button = tk.Button(
            button_frame,
            text="📌 Pin",
            width=12,
            command=self.pin_selected
        )

        self.pin_button.pack(
            side="left",
            padx=5
        )

        # Delete
        self.delete_button = tk.Button(
            button_frame,
            text="🗑 Delete",
            width=12,
            command=self.delete_selected
        )

        self.delete_button.pack(
            side="left",
            padx=5
        )

        # Clear Search
        self.clear_button = tk.Button(
            button_frame,
            text="Clear Search",
            width=12,
            command=self.clear_search
        )

        self.clear_button.pack(
            side="left",
            padx=5
        )

        # ========================================
        # Status
        # ========================================

        self.status_label = tk.Label(
            root,
            text="Ready",
            font=("Arial", 10)
        )

        self.status_label.pack(
            pady=(0, 15)
        )

        # ========================================
        # เริ่ม Clipboard Monitoring
        # ========================================

        self.monitor_clipboard()

    # ========================================
    # Clipboard Monitoring
    # ========================================

    def monitor_clipboard(self):

        # ตรวจสอบ Clipboard
        old_count = len(self.manager.history)

        self.manager.check_clipboard()

        new_count = len(self.manager.history)

        # ถ้ามีข้อมูลใหม่
        if new_count > old_count:

            self.status_label.config(
                text="New clipboard item detected!"
            )

            self.update_history()

        # เรียก function นี้อีกครั้งใน 500 ms
        self.root.after(
            500,
            self.monitor_clipboard
        )

    # ========================================
    # แสดง History
    # ========================================

    def update_history(self):

        keyword = self.search_entry.get().lower()

        self.listbox.delete(
            0,
            tk.END
        )

        for index, item in enumerate(
            self.manager.history
        ):

            # Search
            if keyword and keyword not in item.lower():
                continue

            # เปลี่ยน newline ให้แสดงในบรรทัดเดียว
            preview = item.replace(
                "\n",
                " "
            )

            # จำกัดความยาว
            if len(preview) > 100:

                preview = (
                    preview[:100]
                    + "..."
                )

            # ถ้า Pin ให้แสดง 📌
            if item in self.manager.pinned:

                preview = "📌 " + preview

            self.listbox.insert(
                tk.END,
                preview
            )

        self.status_label.config(
            text=f"Clipboard Items: {len(self.manager.history)}"
        )

    # ========================================
    # STEP 7: Copy Selected
    # ========================================

    def copy_selected(self):

        selection = self.listbox.curselection()

        if not selection:

            messagebox.showwarning(
                "Warning",
                "Please select an item."
            )

            return

        # ปัญหาคือ Search อาจทำให้ index ใน Listbox
        # ไม่ตรงกับ history
        # ดังนั้นหา item จากข้อความที่แสดงแทน

        displayed_text = self.listbox.get(
            selection[0]
        )

        displayed_text = displayed_text.replace(
            "📌 ",
            "",
            1
        )

        # ค้นหา item จริง
        for item in self.manager.history:

            preview = item.replace(
                "\n",
                " "
            )

            if len(preview) > 100:
                preview = preview[:100] + "..."

            if preview == displayed_text:

                pyperclip.copy(item)

                self.status_label.config(
                    text="Copied to clipboard!"
                )

                return

        messagebox.showerror(
            "Error",
            "Could not find selected item."
        )

    # ========================================
    # STEP 8: Delete Selected
    # ========================================

    def delete_selected(self):

        selection = self.listbox.curselection()

        if not selection:
            messagebox.showwarning(
                "Warning",
                "Please select an item."
            )
            return

        displayed_text = self.listbox.get(
            selection[0]
        )

        displayed_text = displayed_text.replace(
            "📌 ",
            "",
            1
        )

        for index, item in enumerate(
            self.manager.history
        ):

            preview = item.replace(
                "\n",
                " "
            )

            if len(preview) > 100:
                preview = preview[:100] + "..."

            if preview == displayed_text:

                self.manager.delete_item(
                    index
                )

                self.update_history()

                self.status_label.config(
                    text="Item deleted."
                )

                return

    # ========================================
    # STEP 9: Pin Selected
    # ========================================

    def pin_selected(self):

        selection = self.listbox.curselection()

        if not selection:

            messagebox.showwarning(
                "Warning",
                "Please select an item."
            )

            return

        displayed_text = self.listbox.get(
            selection[0]
        )

        displayed_text = displayed_text.replace(
            "📌 ",
            "",
            1
        )

        for index, item in enumerate(
            self.manager.history
        ):

            preview = item.replace(
                "\n",
                " "
            )

            if len(preview) > 100:
                preview = preview[:100] + "..."

            if preview == displayed_text:

                if item in self.manager.pinned:

                    messagebox.showinfo(
                        "Pinned",
                        "This item is already pinned."
                    )

                else:

                    self.manager.pin_item(
                        index
                    )

                    self.update_history()

                    self.status_label.config(
                        text="Item pinned!"
                    )

                return

    # ========================================
    # STEP 10: Search
    # ========================================

    def search(self, event=None):

        self.update_history()

    # ========================================
    # Clear Search
    # ========================================

    def clear_search(self):

        self.search_entry.delete(
            0,
            tk.END
        )

        self.update_history()


# ============================================
# เริ่มโปรแกรม
# ============================================

root = tk.Tk()

app = App(root)

root.mainloop()