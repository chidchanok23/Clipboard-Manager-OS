# Clipboard Manager OS

Mini Project สำหรับรายวิชา Operating Systems

Clipboard Manager OS เป็นโปรแกรม Desktop Application ที่พัฒนาด้วย Python โดยสามารถตรวจจับข้อความจาก Clipboard และจัดเก็บเป็น Clipboard History พร้อมจำลองแนวคิดของระบบปฏิบัติการ เช่น Process, Process State, Process Queue, CPU Scheduling, Thread และ Synchronization

---

## Features

### Clipboard Manager

- ตรวจจับข้อความที่ถูก Copy จาก Clipboard
- เก็บ Clipboard History
- Search ข้อความใน History
- Pin / Unpin ข้อความ
- Copy ข้อความกลับไปยัง Clipboard
- Delete ข้อความจาก History

### OS Process Manager

เมื่อมีข้อความใหม่เข้าสู่ Clipboard ระบบจะสร้าง Process ใหม่โดยอัตโนมัติ

แต่ละ Process ประกอบด้วย:

- PID
- Clipboard Content
- Priority
- Process State
- Waiting Time
- Turnaround Time

Process State:

```text
READY → RUNNING → COMPLETED
```

---

## Operating System Concepts

โปรเจกต์นี้ประยุกต์ใช้แนวคิดจากระบบปฏิบัติการดังนี้

### 1. Process Management

ข้อความใหม่จาก Clipboard จะถูกสร้างเป็น Process และกำหนด PID เช่น:

```text
P1
P2
P3
```

Process ใหม่จะเริ่มต้นในสถานะ `READY`

### 2. Process Queue

Process ที่อยู่ในสถานะ READY จะถูกเพิ่มเข้า Process Queue เพื่อรอ Scheduler เลือกไปประมวลผล

### 3. FCFS Scheduling

First Come First Serve เลือก Process ตามลำดับที่เข้าสู่ Queue

ตัวอย่าง:

```text
P1 → P2 → P3
```

### 4. Priority Scheduling

เลือก Process ที่มี Priority สูงกว่าก่อน

ลำดับ Priority:

```text
HIGH → NORMAL → LOW
```

ตัวอย่าง:

```text
P1 = LOW
P2 = HIGH
P3 = NORMAL
```

ลำดับการทำงาน:

```text
P2 → P3 → P1
```

### 5. Process State

แต่ละ Process มีการเปลี่ยนสถานะ:

```text
READY
  ↓
RUNNING
  ↓
COMPLETED
```

### 6. Thread

ใช้ Worker Thread สำหรับจำลองการประมวลผล Process เพื่อไม่ให้ GUI ค้างระหว่างการทำงาน

### 7. Synchronization

ใช้ `threading.Lock` เพื่อควบคุมการเข้าถึง Process Queue และข้อมูลที่ใช้ร่วมกัน ลดปัญหาจากการเข้าถึง Critical Section พร้อมกัน

### 8. Waiting Time and Turnaround Time

ระบบคำนวณ:

```text
Waiting Time
= Start Time - Created Time
```

และ:

```text
Turnaround Time
= Finish Time - Created Time
```

---

## Project Structure

```text
Clipboard-Manager-OS/
│
├── main.py
├── process.py
├── scheduler.py
├── worker.py
├── synchronization.py
├── test_os.py
├── .gitignore
└── README.md
```

### File Description

| File | Description |
|---|---|
| `main.py` | GUI, Clipboard Monitoring และการเชื่อมระบบทั้งหมด |
| `process.py` | Process, Process State และ Time Statistics |
| `scheduler.py` | Process Queue, FCFS และ Priority Scheduling |
| `worker.py` | Worker Thread สำหรับประมวลผล Process |
| `synchronization.py` | Lock สำหรับ Synchronization |
| `test_os.py` | ทดสอบองค์ประกอบหลักของระบบ |

---

## Requirements

- Python 3
- Tkinter
- Pyperclip

ติดตั้ง Pyperclip:

```powershell
python -m pip install pyperclip
```

---

## How to Run

Clone repository:

```powershell
git clone <repository-url>
```

เข้าโฟลเดอร์:

```powershell
cd Clipboard-Manager-OS
```

ติดตั้ง dependency:

```powershell
python -m pip install pyperclip
```

รันโปรแกรม:

```powershell
python main.py
```

---

## How to Use

1. เปิดโปรแกรม Clipboard Manager OS
2. Copy ข้อความจากโปรแกรมอื่น
3. ข้อความจะเข้าสู่ Clipboard History
4. ระบบจะสร้าง Process และเพิ่มเข้า Process Queue
5. เลือก Scheduling Algorithm ระหว่าง FCFS หรือ Priority
6. สามารถกำหนด Priority เป็น HIGH, NORMAL หรือ LOW
7. กด START เพื่อเริ่ม Scheduling
8. สังเกต Process State จาก READY → RUNNING → COMPLETED
9. ตรวจสอบ Waiting Time และ Turnaround Time จาก Statistics

---

## Testing

ระบบได้รับการทดสอบในหัวข้อต่อไปนี้:

- Clipboard Monitoring
- Clipboard History
- Process Creation
- Process Queue
- FCFS Scheduling
- Priority Scheduling
- Process State
- Worker Thread
- Synchronization
- STOP
- CLEAR
- RESET DEMO
- Waiting Time
- Turnaround Time

---

## Important Note

ส่วน Clipboard Monitoring และ Clipboard History ทำงานกับ Clipboard จริงของระบบ

ส่วน Process Scheduling และระยะเวลาการประมวลผลถูกออกแบบเป็น simulation เพื่อใช้สาธิตแนวคิดของระบบปฏิบัติการ โดยโปรแกรมไม่ได้ควบคุม CPU Scheduler จริงของ Windows

---

## Technologies

- Python
- Tkinter
- Pyperclip
- Threading
- Git / GitHub

---

## Project Type

Operating Systems Mini Project