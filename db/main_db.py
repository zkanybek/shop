import sqlite3

conn = sqlite3.connect("tasks.db", check_same_thread=False)
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            completed INTEGER DEFAULT 0,
            quantity INTEGER DEFAULT 1
        )
    ''')
    conn.commit()

def get_tasks():
    cursor.execute("SELECT id, text, completed, quantity FROM tasks")
    return cursor.fetchall()

def add_task_db(task_text, quantity=1):
    cursor.execute("INSERT INTO tasks (text, completed, quantity) VALUES (?, ?, ?)", (task_text, 0, quantity))
    conn.commit()
    return cursor.lastrowid

def update_task_db(task_id, text=None, completed=None, quantity=None):
    if text is not None:
        cursor.execute("UPDATE tasks SET text = ? WHERE id = ?", (text, task_id))
    if completed is not None:
        cursor.execute("UPDATE tasks SET completed = ? WHERE id = ?", (completed, task_id))
    if quantity is not None:
        cursor.execute("UPDATE tasks SET quantity = ? WHERE id = ?", (quantity, task_id))
    conn.commit()

def delete_task_db(task_id):
    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()

def clear_history():
    cursor.execute("DELETE FROM tasks")
    conn.commit()
