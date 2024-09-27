from flask import Flask, jsonify, request, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
  conn = sqlite3.connect('task_management.db')
  conn.row_factory = sqlite3.Row
  return conn

def create_table():
  conn = get_db_connection()
  conn.execute('''
               CREATE TABLE IF NOT EXISTS tasks (
               id INTEGER PRIMARY KEY,
               title TEXT NOT NULL,
               description TEXT,
               due_date DATE NOT NULL,
               priority TEXT NOT NULL,
               completed BOOLEAN NOT NULL DEFAULT 0
               )
              ''')
  conn.commit()
  conn.close()

create_table()

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
  conn = get_db_connection()
  tasks = conn.execute('SELECT * FROM tasks').fetchall()
  conn.close()

  task_list = [dict(task) for task in tasks]
  return jsonify(task_list)

@app.route('/api/tasks', methods=['POST'])
def add_task():
  task_data = request.json
  title = task_data.get('title')
  description = task_data.get('description')
  due_date = task_data.get('due_date')
  priority = task_data.get('priority')

  conn = get_db_connection()
  conn.execute('''
               INSERT INTO tasks (title, description, due_date, priority)
               VALUES (?, ?, ?, ?)
               ''', (title, description, due_date, priority))
  conn.commit()
  conn.close()

  return jsonify({'message': 'Task added successfully!'})

@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def complete_task(task_id):
  conn = get_db_connection()
  conn.execute('''
               UPDATE tasks
               SET completed = 1
               WHERE id = ?
               ''', (task_id,))
  conn.commit()
  conn.close()

  return jsonify({'message': 'Task marked as completed!'}), 200

@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
  conn = get_db_connection()
  conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
  conn.commit()
  conn.close()

  return jsonify({'message': 'Task deleted!'}), 200

def quick_sort(tasks, key):
    if len(tasks) <= 1:
        return tasks
    else:
        pivot = tasks[len(tasks) // 2][key]
        left = [task for task in tasks if task[key] < pivot]
        middle = [task for task in tasks if task[key] == pivot]
        right = [task for task in tasks if task[key] > pivot]
        return quick_sort(left, key) + middle + quick_sort(right, key)

@app.route('/api/tasks/sorted', methods=['GET'])
def get_sorted_tasks():
    sort_by = request.args.get('sort_by', 'priority')  # Default to sorting by priority
    conn = get_db_connection()
    # Build SQL query dynamically based on sorting criteria
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
    
    task_list = [dict(task) for task in sorted_tasks]
    return jsonify(task_list)

@app.route('/')
def index():
  return render_template('index.html')

if __name__ == '__main__':
  app.run(debug=True)