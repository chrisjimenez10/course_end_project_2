# 🦖 Jurassic Adventure

A text-based adventure game where you explore the Dark Forest or Mysterious Cave to find hidden treasure. Your choices earn points — score 650+ to win! Tracks player stats and login history using SQLite.

## **Requirements**

| Component | Minimum Version | Notes |
| --- | --- | --- |
| **Python** | 3.10+ | 3.11+ recommended for full `datetime.fromisoformat()` support |
| **SQLite** | 3.35.0+ | Required for `INSERT ... RETURNING` clause in `db_logic.py` |
| **OS** | Windows / macOS / Linux | Tested on all three |

> **Check your versions:**
> ```macOS/Linux
> python3 --version
> python3 -c "import sqlite3; print(sqlite3.sqlite_version)"
> ```

> ```Windows
> python --version
> python -c "import sqlite3; print(sqlite3.sqlite_version)"
> ```

### **Python Dependencies**
- `pandas` - Handles game choices via CSV
- `tzlocal` - Auto-detects player timezone for login timestamps

Standard library modules used: `sqlite3`, `datetime`, `zoneinfo`, `os`, `time`, `functools`

---

## **Installation & Setup**

### **1. Clone the repository**
* git clone https://github.com/chrisjimenez10/course_end_project_2.git

### **2. Create Virtual Environment**
* cd course_end_project_2
* python -m venv venv
* venv\Scripts\activate
* source venv/bin/activate

### **3. Install Dependencies**
* pip install -r requirements.txt

### **4. Run Game File**
* python main.py



