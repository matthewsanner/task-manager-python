import sqlite3
from config import Config

def get_db_connection():
    conn = sqlite3.connect(Config.DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def create_table():
    conn = get_db_connection()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            due_date DATE NOT NULL,
            priority TEXT NOT NULL,
            completed BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()

# Database interaction functions
def fetch_all_tasks():
    conn = get_db_connection()
    tasks = conn.execute('SELECT * FROM tasks').fetchall()
    conn.close()
    return tasks

def fetch_sorted_tasks(sort_by='priority'):
    conn = get_db_connection()
    
    if sort_by == 'priority':
        sorted_tasks = conn.execute('''
            SELECT * FROM tasks
            ORDER BY 
                CASE priority 
                    WHEN 'High' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Low' THEN 3
                    ELSE 4
                END
        ''').fetchall()
    elif sort_by == 'due_date':
        sorted_tasks = conn.execute('SELECT * FROM tasks ORDER BY due_date').fetchall()
    else:
        sorted_tasks = conn.execute('SELECT * FROM tasks').fetchall()
    
    conn.close()
    return sorted_tasks

def search_tasks(search_term):
    conn = get_db_connection()
    search_term = f"%{search_term}%"  # Format for partial matching in SQL
    query = "SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?"
    found_tasks = conn.execute(query, (search_term, search_term)).fetchall()
    conn.close()
    return found_tasks

def add_task_to_db(title, description, due_date, priority):
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO tasks (title, description, due_date, priority)
        VALUES (?, ?, ?, ?)
    ''', (title, description, due_date, priority))
    conn.commit()
    conn.close()

def mark_task_complete(task_id):
    conn = get_db_connection()
    conn.execute('UPDATE tasks SET completed = 1 WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()

def delete_task_from_db(task_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    conn.commit()
    conn.close()